using System;
using System.Globalization;

internal static class PaygodClock
{
    public static DateTimeOffset UtcNowOffset
    {
        get
        {
            var v = Environment.GetEnvironmentVariable("PAYGOD_CLOCK");
            if (!string.IsNullOrWhiteSpace(v) &&
                DateTimeOffset.TryParse(v, CultureInfo.InvariantCulture,
                    DateTimeStyles.AssumeUniversal | DateTimeStyles.AdjustToUniversal,
                    out var dto))
            {
                return dto;
            }
            var strict = Environment.GetEnvironmentVariable("PAYGOD_STRICT");
if (strict == "1")
{
    throw new InvalidOperationException("PAYGOD_STRICT=1 requires PAYGOD_CLOCK to be set.");
}
return DateTimeOffset.UtcNow;
        }
    }

    public static DateTime UtcNow => UtcNowOffset.UtcDateTime;
}



