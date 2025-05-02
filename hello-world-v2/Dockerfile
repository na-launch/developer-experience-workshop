# STAGE 1: Build
FROM mcr.microsoft.com/dotnet/sdk:9.0 AS build
WORKDIR /src

ENV ASPNETCORE_ENVIRONMENT=Production
ENV countryCode=EN
ENV ASPNETCORE_URLS=http://+:8080


# Copy the project file and restore dependencies
COPY ["ds-challenge-04.csproj", "./"]
RUN dotnet restore "ds-challenge-04.csproj"

# Copy the rest of the source code and publish the app
COPY . .
RUN dotnet publish "ds-challenge-04.csproj" -c Release -o /app/publish

# STAGE 2: Runtime
FROM mcr.microsoft.com/dotnet/aspnet:9.0 AS runtime
WORKDIR /app
COPY --from=build /app/publish .



# Set the container entry point to run the published DLL.
ENTRYPOINT ["dotnet", "ds-challenge-04.dll"]