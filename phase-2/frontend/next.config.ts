import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Enable standalone output for Docker builds
  output: "standalone",
  // Temporarily disable React Compiler to test auth flow
  // reactCompiler: true,
  serverExternalPackages: ["pg"],
};

export default nextConfig;
