from datetime import datetime, timedelta
import re

class TimeExpressionFSA:
    def __init__(self, today=None):
        self.today = today or datetime.now()
        self.current_base_date = None  # To track the base date/time for dependencies

        self.states = {
            "start": "Initial state",
            "relative_days": "Matches relative days",
            "week_based": "Matches week-based expressions",
            "absolute_dates": "Matches absolute dates",
            "relative_time": "Matches relative time expressions",
            "time": "Matches time",
            "end": "Final state"
        }

        self.patterns = {
            "relative_days": r"\b(yesterday|today|tomorrow)\b",
            "week_based": r"\b(on|next|this|last)? ?(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\b",
            "absolute_dates": r"\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\.? \d{1,2}(?:st|nd|rd|th)?,? \d{2,4}|\d{1,2}(?:st|nd|rd|th)? (Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?))\b",
            "relative_time": r"\b(\d+) (min|minute|hour|day|week|month|year)s? ?(ago|from now|later)?\b",
            "time": r"\b(at\s?)?(\d{1,2})[:.](\d{2})\s?(am|pm)?\b"
        }

    def process_input(self, text):
        matches = []
        # Prioritize categories to prevent misclassification
        categories = ["relative_time", "relative_days", "week_based", "absolute_dates", "time"]
        for category in categories:
            pattern = self.patterns[category]
            for match in re.finditer(pattern, text, re.IGNORECASE):
                matches.append((category, match.group()))
        return matches

    def calculate_combined_datetime(self, matches):
        for category, expression in matches:
            resulting_date = self.calculate_date(expression, category)
            print("Initial resulting date: ", resulting_date)
            if category in ["relative_days", "week_based", "absolute_dates", "relative_time"]:
                # Set the base date if a "date-like" expression is found
                self.current_base_date = resulting_date
            elif category == "time" and self.current_base_date:
                # Combine time with the base date
                self.current_base_date = self._combine_time_with_base(self.current_base_date, resulting_date)
            elif category == "time":
                # If no base date, just set the time
                self.current_base_date = resulting_date
        return self.current_base_date

    def calculate_date(self, expression, category):
        if category == "relative_days":
            return self._calculate_relative_days(expression)
        elif category == "week_based":
            return self._calculate_week_based(expression)
        elif category == "absolute_dates":
            return self._parse_absolute_date(expression)
        elif category == "relative_time":
            return self._calculate_relative_time(expression)
        elif category == "time":
            return self._parse_time(expression)
        return None

    def _combine_time_with_base(self, base_date, time):
        if not base_date or not time:
            return None
        return base_date.replace(hour=time.hour, minute=time.minute, second=0, microsecond=0)

    def _calculate_relative_days(self, expression):
        if expression.lower() == "yesterday":
            return self.today - timedelta(days=1)
        elif expression.lower() == "today":
            return self.today
        elif expression.lower() == "tomorrow":
            return self.today + timedelta(days=1)

    def _calculate_week_based(self, expression):
        match = re.match(r"(on|next|this|last|coming)? ?(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)", expression, re.IGNORECASE)
        if not match:
            return None
        direction, day = match.groups()
        days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        target_weekday = days_of_week.index(day.capitalize())
        current_weekday = self.today.weekday()

        if not direction or direction.lower() in ["this", "on"]:
            delta = (target_weekday - current_weekday + 7) % 7
        elif direction.lower() == "next" or direction.lower() == "coming":
            delta = (target_weekday - current_weekday + 7) % 7 or 7
        elif direction.lower() == "last":
            delta = -((current_weekday - target_weekday + 7) % 7 or 7)
        return self.today + timedelta(days=delta)

    def _parse_absolute_date(self, expression):
        # Regular expression to match various absolute date formats
        absolute_dates_pattern = r"\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\.? \d{1,2}(?:st|nd|rd|th)?,? \d{2,4}|\d{1,2}(?:st|nd|rd|th)? (Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?))\b"
        
        # Remove any ordinal suffixes (st, nd, rd, th)
        def preprocess_date(date_str):
            return re.sub(r'(st|nd|rd|th)', '', date_str, flags=re.IGNORECASE).strip()

        # Try to find all date matches
        matches = re.findall(absolute_dates_pattern, expression, re.IGNORECASE)
        if not matches:
            return None  # Return None if no matches found

        # For each match, try parsing the date
        for match in matches:
            date_str = match[0]  # The first group is the full match
            date_str = preprocess_date(date_str)  # Remove ordinal suffixes
            current_date = self.today or datetime.now()  # Use today's date if not provided

            # Try different date formats
            for fmt in ("%d/%m/%Y", "%d-%m-%Y", "%d/%m/%y", "%d/%m/%y", "%B %d, %Y", "%B %d %Y", "%b %d, %Y", "%b %d %Y", "%d %b %Y", "%d %B", "%B %d", "%b %d", "%d %b"):
                try:
                    parsed_date = datetime.strptime(date_str, fmt)
                    # Handle formats without a year (e.g., "25 December")
                    if fmt in ("%d %B", "%d %b", "%B %d", "%b %d"):
                        parsed_date = parsed_date.replace(year=current_date.year)
                        # If the date has already passed this year, assign it to the next year
                        if parsed_date < current_date:
                            parsed_date = parsed_date.replace(year=current_date.year + 1)
                    
                    return parsed_date  # Return the successfully parsed date
                except ValueError:
                    continue  # Try the next format

        return None
    
    def _calculate_relative_time(self, expression):
        match = re.match(r"(\d+) (min|minute|hour|day|week|month|year)s? ?(ago|from now|later)?", expression, re.IGNORECASE)
        if not match:
            return None
        value, unit, direction = match.groups()
        value = int(value)
        delta = {
            "minute": timedelta(minutes=value),
            "hour": timedelta(hours=value),
            "day": timedelta(days=value),
            "week": timedelta(weeks=value),
            "month": timedelta(days=value * 30),
            "year": timedelta(days=value * 365),
        }.get(unit.lower(), timedelta(0))
        return self.today + delta if direction in {"later", "from now"} else self.today - delta

    def _parse_time(self, expression):
        match = re.match(r"\b(at\s?)?(\d{1,2})[:.](\d{2})\s?(am|pm)?\b", expression, re.IGNORECASE)
        if not match:
            return None
        _, hour, minute, period = match.groups()
        hour = int(hour)
        minute = int(minute) if minute else 0
        if period:
            if period.lower() == "pm" and hour != 12:
                hour += 12
            elif period.lower() == "am" and hour == 12:
                hour = 0
        return datetime.now().replace(hour=hour, minute=minute, second=0, microsecond=0)

# Example usage
if __name__ == "__main__":
    fsa = TimeExpressionFSA()
    test_text = "10 minute ago"
    matches = fsa.process_input(test_text)
    final_date = fsa.calculate_combined_datetime(matches)
    if final_date:
        print(f"Final Date and Time: {final_date.strftime('%A, %d %B %Y %I:%M %p')}")
    else:
        print("No valid date found.")