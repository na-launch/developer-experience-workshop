using Microsoft.AspNetCore.SignalR;

public record ChangeTopicRequest(string topic);

public static class KafkaTopicManager
    {
        // Holds the current topic for the Kafka consumer.
        private static string _currentTopic = "test-topic";

        public static string CurrentTopic
        {
            get => _currentTopic;
            set
            {
                if (!string.IsNullOrWhiteSpace(value))
                {
                    _currentTopic = value;
                    Console.WriteLine($"Current Kafka topic updated to: {_currentTopic}");
                }
            }
        }
    }
    

public class KafkaHub : Hub
{
    public override Task OnConnectedAsync()
    {
        Console.WriteLine("SignalR connection established.");
        return base.OnConnectedAsync();
    }


    public async Task SendMessage(string message)
    {
        await Clients.All.SendAsync("ReceiveMessage", message);
    }
}
