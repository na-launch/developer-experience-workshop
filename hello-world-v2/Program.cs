using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Hosting;
using System;
using System.Collections.Generic;

namespace ds_challenge_04
{
    public class Program
    {
        public static void Main(string[] args)
        {
            var builder = WebApplication.CreateBuilder(args);
            
            // If you want to use controllers or static files, register those services.
            builder.Services.AddControllers(); // Not strictly required in this minimal example.

            var app = builder.Build();

            if (app.Environment.IsDevelopment())
            {
                app.UseDeveloperExceptionPage();
                app.UseHttpsRedirection();
            }
            else
            {
                app.UseExceptionHandler("/Home/Error");
                app.UseHsts();
            }

            // You can serve static files if needed.
            // app.UseStaticFiles();

            // Minimal API endpoint that returns an HTML page.
            app.MapGet("/", (HttpContext context) =>
            {
                // Dictionary for translations.
                var translations = new Dictionary<string, string>
                {
                    { "EN", "Hello World!" },
                    { "SP", "¡Hola Mundo!" },
                    { "FR", "Bonjour le monde!" },
                    { "DE", "Hallo Welt!" },
                    { "IT", "Ciao Mondo!" },
                    { "SW", "Hej världen!" }
                };

                // Dictionary for flag image URLs.
                var flags = new Dictionary<string, string>
                {
                    { "EN", "https://flagcdn.com/w320/us.png" },  // US flag for English
                    { "SP", "https://flagcdn.com/w320/es.png" },
                    { "FR", "https://flagcdn.com/w320/fr.png" },
                    { "DE", "https://flagcdn.com/w320/de.png" },
                    { "IT", "https://flagcdn.com/w320/it.png" },
                    { "SW", "https://flagcdn.com/w320/se.png" }   // Swedish flag (adjust if needed)
                };

                // Read the country code from the environment variable (default to "EN").
                var country = Environment.GetEnvironmentVariable("countryCode") ?? "EN";
                if (country.Length != 2)
                {
                    country = "EN";
                }
                country = country.ToUpper();

                // Lookup translation and flag.
                translations.TryGetValue(country, out string greeting);
                greeting = greeting ?? "Hello World!";
                string flagUrl = flags.ContainsKey(country) ? flags[country] : flags["EN"];

                // Build an HTML page that displays the greeting with the flag.
                var html = $@"
<!DOCTYPE html>
<html lang=""en"">
<head>
  <meta charset=""UTF-8"">
  <meta name=""viewport"" content=""width=device-width, initial-scale=1.0"">
  <title>Hello World Translation</title>
  <style>
    body {{
      font-family: Arial, sans-serif;
      text-align: center;
      padding-top: 50px;
      background-color: #f4f4f4;
    }}
    h1 {{
      font-size: 2.5em;
      color: #333;
    }}
    .flag {{
      width: 80px;
      vertical-align: middle;
      margin-left: 20px;
      border: 1px solid #ccc;
    }}
  </style>
</head>
<body>
  <h1>
    {greeting}
    <img class=""flag"" src=""{flagUrl}"" alt=""Flag of {country}"">
  </h1>
</body>
</html>
";

                return Results.Content(html, "text/html");
            });

            app.Run();
        }
    }
}