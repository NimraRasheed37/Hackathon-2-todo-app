import { NextResponse } from "next/server";

/**
 * Health check endpoint for Kubernetes probes.
 * Returns 200 if the frontend application is running.
 *
 * Used for:
 * - Kubernetes liveness probe
 * - Kubernetes readiness probe
 * - Load balancer health checks
 */
export async function GET() {
  return NextResponse.json({
    status: "healthy",
    timestamp: new Date().toISOString(),
  });
}
