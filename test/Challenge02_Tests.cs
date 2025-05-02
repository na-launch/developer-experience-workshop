using ds_challenge02.Controllers;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Configuration;  // Added for AddInMemoryCollection
using System.Collections.Generic;
using System.IO;
using System.Net;
using System.Net.Http;
using System.Text.Json;
using System.Threading;
using System.Threading.Tasks;
using Xunit;

namespace Challenge2Tests
{
    public class Challenge02_Tests
    {
        [Fact]
        public void VersionController_ReturnsCorrectVersion()
        {
            // Arrange
            var controller = new ds_challenge02.Controllers.Version();

            // Act
            var result = controller.version();

            // Assert
            Assert.Equal("0.0.1", result);
        }

        [Fact]
        public void HealthController_ReturnsHealthyStatus()
        {
            // Arrange
            var controller = new HealthController();

            // Act
            IActionResult actionResult = controller.GetHealth();

            // Assert
            var okResult = Assert.IsType<OkObjectResult>(actionResult);
            Assert.NotNull(okResult.Value); // ensure not null to avoid dereference warning

            var value = okResult.Value;
            // Use reflection to access the anonymous object's properties.
            var messageProperty = value!.GetType().GetProperty("message");
            var versionProperty = value!.GetType().GetProperty("version");

            Assert.NotNull(messageProperty);
            Assert.NotNull(versionProperty);

            var messageValue = messageProperty.GetValue(value) as string;
            var versionValue = versionProperty.GetValue(value) as string;

            Assert.Equal("Service is healthy", messageValue);
            Assert.Equal("0.0.1", versionValue);
        }

        // Helper to create an in-memory configuration.
        private IConfiguration GetTestConfiguration(string adminUrl)
        {
            var inMemorySettings = new Dictionary<string, string>
            {
                { "ADMIN", adminUrl }
            };
            return new ConfigurationBuilder()
                .AddInMemoryCollection(inMemorySettings)
                .Build();
        }

        // Fake HttpMessageHandler for testing the AdminController.
        public class FakeHttpMessageHandler : HttpMessageHandler
        {
            private readonly HttpResponseMessage _response;

            public FakeHttpMessageHandler(HttpResponseMessage response)
            {
                _response = response;
            }

            protected override Task<HttpResponseMessage> SendAsync(HttpRequestMessage request, CancellationToken cancellationToken)
            {
                return Task.FromResult(_response);
            }
        }

        [Fact]
        public async Task AdminController_IncorrectPassword_Returns403()
        {
            // Arrange
            var config = GetTestConfiguration("http://example.com");
            var httpClient = new HttpClient(new FakeHttpMessageHandler(new HttpResponseMessage(HttpStatusCode.OK)
            {
                Content = new StringContent("{\"dummy\":\"value\"}")
            }));
            var controller = new AdminController(config, httpClient);

            // Act
            var result = await controller.GetAdmin("wrongpassword");

            // Assert
            var objectResult = Assert.IsType<ObjectResult>(result);
            Assert.Equal(403, objectResult.StatusCode);
        }

        [Fact]
        public async Task AdminController_CorrectPassword_ReturnsFormattedJson()
        {
            // Arrange
            string fakeJson = "{\"key\":\"value\"}";
            var config = GetTestConfiguration("http://dummyadmin/api");
            var responseMessage = new HttpResponseMessage(HttpStatusCode.OK)
            {
                Content = new StringContent(fakeJson)
            };
            var httpClient = new HttpClient(new FakeHttpMessageHandler(responseMessage));
            var controller = new AdminController(config, httpClient);

            // Act
            var result = await controller.GetAdmin("opensesame");

            // Assert
            var contentResult = Assert.IsType<ContentResult>(result);
            Assert.Equal("text/html", contentResult.ContentType);
            Assert.Contains("<pre>", contentResult.Content);
            Assert.Contains("value", contentResult.Content);
        }

        [Fact]
        public async Task TranslationController_ReturnsTranslation_WhenCountryExists()
        {
            // Arrange
            // Write a temporary translations.json file with a known translation.
            string tempFile = "translations.json";
            var translationsData = new
            {
                translations = new Dictionary<string, string>
                {
                    { "EN", "Hello" }
                }
            };
            string jsonContent = JsonSerializer.Serialize(translationsData);
            await File.WriteAllTextAsync(tempFile, jsonContent);

            try
            {
                var controller = new TranslationController
                {
                    // Set the high-level CountryCode property (default: "en")
                    CountryCode = "en"
                };

                // Act
                var result = await controller.GetTranslation();

                // Assert
                var okResult = Assert.IsType<OkObjectResult>(result);
                var content = okResult.Value as string;
                Assert.NotNull(content);
                Assert.Contains("Hello", content);
                Assert.Contains("@", content); // Checks for timestamp
            }
            finally
            {
                // Clean up the temporary file.
                if (File.Exists(tempFile))
                    File.Delete(tempFile);
            }
        }

        [Fact]
        public async Task TranslationController_ReturnsNotFound_WhenCountryDoesNotExist()
        {
            // Arrange
            // Create a temporary translations.json file with translation data for another country.
            string tempFile = "translations.json";
            var translationsData = new
            {
                translations = new Dictionary<string, string>
                {
                    { "FR", "Bonjour" }
                }
            };
            string jsonContent = JsonSerializer.Serialize(translationsData);
            await File.WriteAllTextAsync(tempFile, jsonContent);

            try
            {
                var controller = new TranslationController
                {
                    // Set to a country code not present in the file.
                    CountryCode = "en"
                };

                // Act
                var result = await controller.GetTranslation();

                // Assert
                Assert.IsType<NotFoundObjectResult>(result);
            }
            finally
            {
                // Clean up the temporary file.
                if (File.Exists(tempFile))
                    File.Delete(tempFile);
            }
        }
    }
}
