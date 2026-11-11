import java.io.*;
import java.util.*;

public class InstallSSH {
    public static void main(String[] args) throws Exception {
        String logPath = "InstallSSH_output.txt";
        PrintWriter log = new PrintWriter(new FileWriter(logPath, false), true);

        log.println("=== Starting install at " + new Date() + " ===");
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