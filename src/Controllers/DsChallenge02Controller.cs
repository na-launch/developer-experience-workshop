using System.Text.Json;
using Microsoft.AspNetCore.Mvc;

namespace ds_challenge02.Controllers;


[ApiController]
[Route("api/version")]
public class Version : ControllerBase
{
    [HttpGet(Name = "version")]
    public String version()
    {
        return "0.0.1";
    }
}

[ApiController]
[Route("api/health")]
public class HealthController : ControllerBase
{
    [HttpGet(Name = "health")]
    public IActionResult GetHealth()
    {
        // This will return a 200 OK with the provided message.
        return Ok(new { message = "Service is healthy", version = "0.0.1" });
    }
}

[ApiController]
[Route("api/admin")]
public class AdminController : ControllerBase
{
    private readonly IConfiguration _config;
    private readonly HttpClient _httpClient;

    public AdminController(IConfiguration config, HttpClient httpClient)
    {
        _config = config;
        _httpClient = httpClient;
    }

    [HttpGet(Name = "admin")]
    public async Task<IActionResult> GetAdmin([FromQuery] string password)
    {
        // Check if the provided password is correct
        if (password != "opensesame")
        {
            return StatusCode(403, "Forbidden: Incorrect password");
        }

        // Retrieve the admin URL from configuration
        var adminUrl = _config["ADMIN"];
        if (string.IsNullOrEmpty(adminUrl))
        {
            return Problem("ADMIN environment variable not set");
        }

        try
        {
            // Call the external API
            var response = await _httpClient.GetAsync(adminUrl);
            if (!response.IsSuccessStatusCode)
            {
                return Problem("There was a problem calling the API, please review your parameters");
            }

            var jsonString = await response.Content.ReadAsStringAsync();
            using var jsonDoc = JsonDocument.Parse(jsonString);
            var formattedJson = JsonSerializer.Serialize(jsonDoc, new JsonSerializerOptions { WriteIndented = true });

            // Return the JSON wrapped in <pre> tags for HTML formatting
            return Content($"<pre>{formattedJson}</pre>", "text/html");
        }
        catch
        {
            return Problem("Internal server error");
        }
    }
}

[ApiController]
[Route("/")]
public class TranslationController : ControllerBase
{

    public string CountryCode { get; set; } = "en";

    [HttpGet]
    public async Task<IActionResult> GetTranslation()
    {
        string countryCode=CountryCode;
        
        // Return a 400 Bad Request if the country code parameter is missing.
        if (string.IsNullOrEmpty(countryCode))
        {
            return BadRequest("Country code parameter is required.");
        }

        try
        {
            // Read the translations.json file asynchronously.
            string json = await System.IO.File.ReadAllTextAsync("translations.json");

            // Deserialize the JSON into a dictionary where "translations" is a nested dictionary.
            var jsonObject = JsonSerializer.Deserialize<Dictionary<string, Dictionary<string, string>>>(json);

            if (jsonObject != null && jsonObject.TryGetValue("translations", out var translations))
            {
                // Check if the specified country code exists (case-insensitively).
                if (translations.TryGetValue(countryCode.ToUpper(), out var translation))
                {
                    // Build the response with a 200 OK status.
                    var timestamp = DateTime.UtcNow.ToString("o"); // ISO 8601 format
                    return Ok($"{translation} @ {timestamp}");
                }
                else
                {
                    // Return a 404 Not Found if the translation is missing.
                    return NotFound("Translation not found for the specified country code.");
                }
            }
            else
            {
                // Return a 500 Internal Server Error if the JSON format is invalid.
                return StatusCode(500, "Invalid JSON format.");
            }
        }
        catch (Exception ex)
        {
            // Return a 500 Internal Server Error if an exception occurs.
            return StatusCode(500, $"Error: {ex.Message}");
        }
    }
}


// TODO's
// "/api/query"
// "/api/query"
// "/api/magic8"
