import json
import pandas as pd


class TelegramParser:
    """Parses standard Telegram JSON exports."""

    @staticmethod
    def parse(file_content: bytes) -> pd.DataFrame:
        data = json.loads(file_content)
        messages = data.get("messages", [])

        parsed_data = []
        for msg in messages:
            if msg.get("type") == "message" and "from" in msg and "text" in msg:
                # Handle cases where text is a list of strings/entities
                text_content = msg["text"]
                if isinstance(text_content, list):
                    text_content = " ".join(
                        [
                            m if isinstance(m, str) else m.get("text", "")
                            for m in text_content
                        ]
                    )

                parsed_data.append(
                    {
                        "date": pd.to_datetime(msg["date"]),
                        "sender": msg["from"],
                        "text": text_content,
                        "text_length": len(text_content),
                    }
                )

        df = pd.DataFrame(parsed_data)
        if not df.empty:
            df.set_index("date", inplace=True)
            df.sort_index(inplace=True)
        return df
