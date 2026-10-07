package dev.devoxx.pixoo;

import io.github.glaforge.jixoo.image.GifDecoder;
import io.github.glaforge.jixoo.image.GifEncoder;
import io.github.glaforge.jixoo.model.PixooAnimation;
import io.github.glaforge.jixoo.model.PixooFrame;

import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Comparator;
import java.util.List;
import java.util.Locale;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public final class ArtworkTool {
    private static final int SIZE = 64;
    private static final int MAX_FRAMES = 30;
    private static final long MAX_FILE_BYTES = 5L * 1024 * 1024;
    // A frame named like frame_07_600ms.png overrides the default delay.
    private static final Pattern FRAME_DELAY = Pattern.compile("_(\\d+)ms\\.png$", Pattern.CASE_INSENSITIVE);

    private ArtworkTool() {}

    public static void main(String[] args) throws IOException {
        if (args.length == 4 && args[0].equals("compose")) {
            compose(Path.of(args[1]), Path.of(args[2]), Integer.parseInt(args[3]));
        } else if (args.length == 2 && args[0].equals("inspect")) {
            inspect(Path.of(args[1]));
        } else {
            System.err.println("Usage: compose <frames-dir> <output.gif> <default-delay-ms> | inspect <image.png|animation.gif>");
            System.exit(2);
        }
    }

    private static void compose(Path framesDir, Path output, int delayMs) throws IOException {
        if (delayMs < 10 || delayMs % 10 != 0) {
            throw new IllegalArgumentException("GIF frame delay must be a positive multiple of 10 ms");
        }

        List<Path> framePaths;
        try (var paths = Files.list(framesDir)) {
            framePaths = paths
                    .filter(path -> path.getFileName().toString().toLowerCase(Locale.ROOT).endsWith(".png"))
                    .sorted(Comparator.comparing(path -> path.getFileName().toString()))
                    .toList();
        }
        if (framePaths.isEmpty() || framePaths.size() > MAX_FRAMES) {
            throw new IllegalArgumentException("Expected 1 to " + MAX_FRAMES + " PNG frames");
        }

        List<PixooFrame> frames = framePaths.stream().map(path -> {
            try {
                BufferedImage image = ImageIO.read(path.toFile());
                requireSize(image, path);
                return PixooFrame.fromImage(image, frameDelay(path, delayMs));
            } catch (IOException e) {
                throw new IllegalStateException("Cannot read " + path, e);
            }
        }).toList();

        byte[] gif = GifEncoder.encode(new PixooAnimation(frames));
        if (gif.length > MAX_FILE_BYTES) {
            throw new IllegalArgumentException("GIF exceeds the contest's 5 MiB upload limit");
        }
        Path parent = output.getParent();
        if (parent != null) Files.createDirectories(parent);
        Files.write(output, gif);
        inspect(output);
    }

    private static int frameDelay(Path path, int defaultMs) {
        Matcher matcher = FRAME_DELAY.matcher(path.getFileName().toString());
        if (!matcher.find()) return defaultMs;
        int delayMs = Integer.parseInt(matcher.group(1));
        if (delayMs < 10 || delayMs % 10 != 0) {
            throw new IllegalArgumentException(path + ": frame delay must be a positive multiple of 10 ms");
        }
        return delayMs;
    }

    private static void inspect(Path file) throws IOException {
        long bytes = Files.size(file);
        if (bytes > MAX_FILE_BYTES) {
            throw new IllegalArgumentException(file + " exceeds the contest's 5 MiB upload limit");
        }

        String name = file.getFileName().toString().toLowerCase(Locale.ROOT);
        if (name.endsWith(".gif")) {
            byte[] header;
            try (var input = Files.newInputStream(file)) {
                header = input.readNBytes(10);
            }
            if (header.length < 10) throw new IllegalArgumentException("Invalid GIF: " + file);
            int width = (header[6] & 0xff) | ((header[7] & 0xff) << 8);
            int height = (header[8] & 0xff) | ((header[9] & 0xff) << 8);
            requireSize(width, height, file);

            PixooAnimation animation = GifDecoder.decode(file);
            if (animation.frameCount() > MAX_FRAMES) {
                throw new IllegalArgumentException("GIF has more than " + MAX_FRAMES + " frames; Pixoo may loop early");
            }
            int durationMs = animation.frames().stream().mapToInt(PixooFrame::delayMs).sum();
            System.out.printf("%s: 64×64 GIF, %d frames, %.2f s, %d bytes%n",
                    file, animation.frameCount(), durationMs / 1000.0, bytes);
        } else if (name.endsWith(".png")) {
            BufferedImage image = ImageIO.read(file.toFile());
            requireSize(image, file);
            System.out.printf("%s: 64×64 PNG, %d bytes%n", file, bytes);
        } else {
            throw new IllegalArgumentException("Inspect supports PNG and GIF: " + file);
        }
    }

    private static void requireSize(BufferedImage image, Path file) {
        if (image == null) throw new IllegalArgumentException("Cannot decode image: " + file);
        requireSize(image.getWidth(), image.getHeight(), file);
    }

    private static void requireSize(int width, int height, Path file) {
        if (width != SIZE || height != SIZE) {
            throw new IllegalArgumentException(file + " is " + width + "×" + height + "; expected 64×64");
        }
    }
}
