using System;
using System.Threading.Tasks;

class Program
{
    static async Task Main(string[] args)
    {
        // Ensure a mode argument is provided ("produce" or "consume").
        if (args.Length == 0 || string.IsNullOrWhiteSpace(args[0]))
        {
            Console.WriteLine("Usage: dotnet run <produce|consume> [--topic <topic>]");
            return;
        }

        // Default topic value
        string topic = "test-topic";

        // Parse additional command-line arguments for the optional --topic parameter.
        for (int i = 1; i < args.Length; i++)
        {
            if (args[i] == "--topic" && i + 1 < args.Length)
            {
                topic = args[i + 1];
                i++;  // Skip the topic value since it's already processed
            }
        }

        // Select mode.
        if (args[0].Equals("produce", StringComparison.OrdinalIgnoreCase))
        {
            await Producer.Run(topic);
        }
        else if (args[0].Equals("consume", StringComparison.OrdinalIgnoreCase))
        {
            Consumer.Run(topic);
        }
        else
        {
            Console.WriteLine("Usage: dotnet run <produce|consume> [--topic <topic>]");
        }
    }
}
