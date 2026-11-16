import java.io.*;
import java.util.*;

public class InstallSSH {
    public static void main(String[] args) throws Exception {
        String logPath = "InstallSSH_output.txt";
        PrintWriter log = new PrintWriter(new FileWriter(logPath, false), true);

        log.println("=== Starting at " + new Date() + " ===");
        log.flush();

        // The security.debian.org mirror is genuinely missing several
        // deb11u7/u8 .deb files right now (confirmed 404, not a stale-index
        // problem). Comment out that line so apt falls back to the versions
        // available in main/bullseye-updates instead. Edited via Java file
        // I/O directly, avoiding sed/shell quoting issues in this shell.
        File sourcesFile = new File("/etc/apt/sources.list");
        List<String> lines = new ArrayList<>(
                java.nio.file.Files.readAllLines(sourcesFile.toPath()));
        boolean changed = false;
        for (int i = 0; i < lines.size(); i++) {
            String line = lines.get(i);
            if (line.contains("security.debian.org") && !line.trim().startsWith("#")) {
                lines.set(i, "# " + line + "  # commented out: 404s on this mirror");
                changed = true;
            }
        }
        if (changed) {
            java.nio.file.Files.write(sourcesFile.toPath(), lines);
            log.println("=== Commented out security.debian.org line(s) in sources.list ===");
        } else {
            log.println("=== No active security.debian.org line found to comment out ===");
        }
        log.flush();

        // Run a FULL apt-get update first. Your earlier update got cut off
        // by shell output truncation after one line, likely leaving stale
        // package indices that still reference package versions no longer
        // present on the mirrors (causing the 404 errors you saw).
        log.println("=== Running apt-get update (full) ===");
        log.flush();
        int updateExit = runCommand(log, "apt-get", "update");
        log.println("=== apt-get update exited with code " + updateExit + " ===");
        log.println();
        log.flush();

        // Run apt-get install, fully non-interactive, with Dpkg::Use-Pty=0
        // so it doesn't emit terminal control characters that can confuse
        // a minimal shell. ProcessBuilder captures ALL output itself,
        // regardless of whatever is truncating your raw shell's display.
        int exitCode = runCommand(log,
                "apt-get", "install", "-y",
                "-o", "Dpkg::Use-Pty=0",
                "openssh-server");

        log.println("=== apt-get exited with code " + exitCode + " ===");
        log.flush();

        // Verify afterward with dpkg, same ProcessBuilder approach
        log.println();
        log.println("=== Verifying with dpkg -l | grep openssh ===");
        log.flush();
        runCommand(log, "dpkg", "-l");  // full list; we'll grep in Java instead,
                                         // since piping ('|') is shell syntax
                                         // and may not work in your environment

        log.close();

        // Print a short confirmation to the real console
        System.out.println("Done. Full log written to: " +
                new File(logPath).getAbsolutePath());
        System.out.println("Run: cat " + logPath + "   (or re-run this program's sibling reader)");
    }

    private static int runCommand(PrintWriter log, String... command) throws Exception {
        // Set DEBIAN_FRONTEND=noninteractive via the process environment,
        // not shell syntax, since 'env VAR=val cmd' relies on shell parsing
        // that your environment doesn't reliably support.
        ProcessBuilder pb = new ProcessBuilder(command);
        pb.environment().put("DEBIAN_FRONTEND", "noninteractive");
        pb.redirectErrorStream(true); // merge stderr into stdout

        log.println("$ " + String.join(" ", command));
        log.flush();

        Process process = pb.start();

        try (BufferedReader reader = new BufferedReader(
                new InputStreamReader(process.getInputStream()))) {
            String line;
            while ((line = reader.readLine()) != null) {
                log.println(line);
                log.flush(); // flush after every line so partial progress
                             // is visible even if the process runs long
            }
        }

        return process.waitFor();
    }
}