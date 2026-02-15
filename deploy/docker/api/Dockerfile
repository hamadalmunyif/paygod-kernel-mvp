# =========================
# Stage 1 - Build
# =========================
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src

# Copy full repo
COPY . .

# Publish CLI (explicit)
RUN dotnet publish ./src/PayGod.Cli/PayGod.Cli.csproj -c Release -o /app/runner /p:UseAppHost=false

# Publish API (explicit)
RUN dotnet publish ./deploy/docker/api/app/PayGod.Api.csproj -c Release -o /app/api /p:UseAppHost=false

# =========================
# Stage 2 - Runtime
# =========================
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS runtime

# non-root user (API allowed; runner already non-root in its own image)
RUN addgroup --system paygod && adduser --system --ingroup paygod paygod

WORKDIR /app
COPY --from=build /app/api .
COPY --from=build /app/runner /runner

RUN chown -R paygod:paygod /app /runner
USER paygod

EXPOSE 8080
ENTRYPOINT ["dotnet","PayGod.Api.dll"]
