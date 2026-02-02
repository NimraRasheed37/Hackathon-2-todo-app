import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Temporarily disable React Compiler to test auth flow
  // reactCompiler: true,
  serverExternalPackages: ["pg"],
};

export default nextConfig;
