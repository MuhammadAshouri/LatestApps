FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS base
USER $APP_UID
WORKDIR /app
EXPOSE 443

FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
ARG BUILD_CONFIGURATION=Release
WORKDIR /src
COPY ["LatestVpnVersion/LatestVpnVersion.csproj", "LatestVpnVersion/"]
RUN dotnet restore "LatestVpnVersion/LatestVpnVersion.csproj"
COPY . .
WORKDIR "/src/LatestVpnVersion"
RUN dotnet build "LatestVpnVersion.csproj" -c $BUILD_CONFIGURATION -o /app/build

FROM build AS publish
ARG BUILD_CONFIGURATION=Release
RUN dotnet publish "LatestVpnVersion.csproj" -c $BUILD_CONFIGURATION -o /app/publish /p:UseAppHost=false

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "LatestVpnVersion.dll"]
