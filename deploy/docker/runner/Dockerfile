# =========================
# Stage 1 — Build
# =========================
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src

# Copy full repo
COPY . .

# Publish explicit CLI project only (no implicit sln)
RUN dotnet publish ./src/PayGod.Cli/PayGod.Cli.csproj -c Release -o /app/publish /p:UseAppHost=false

# =========================
# Stage 2 — Runtime (Sealed)
# =========================
FROM mcr.microsoft.com/dotnet/runtime:8.0 AS runtime

# non-root user
RUN addgroup --system paygod && adduser --system --ingroup paygod paygod

WORKDIR /app
COPY --from=build /app/publish .

RUN chown -R paygod:paygod /app
USER paygod

# Runner CLI entrypoint (dotnet)
ENTRYPOINT ["dotnet", "PayGod.Cli.dll"]
