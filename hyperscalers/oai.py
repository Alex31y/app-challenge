import base64
from typing import Optional, Dict, List, Union

from openai import OpenAI


class LocalImageAnalyzer:
    def __init__(self, api_key: Optional[str] = None):
        """Initialize with optional API key (otherwise uses environment variable)"""
        self.client = OpenAI(api_key=api_key)

    def encode_image(self, image_path: str) -> str:
        """Convert local image to base64 string"""
        try:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        except Exception as e:
            raise Exception(f"Error reading image file: {str(e)}")

    def analyze_image(
            self,
            image_path: Union[str, List[str]],
            prompt: str = "What's in this image?",
            model: str = "gpt-4o-mini",
            # max_tokens: int = 300
    ) -> str:
        """
        Analyze one or multiple local images using OpenAI's API.

        Args:
            image_path: Single path or list of paths to local image files
            user_prompt: Question or prompt about the image(s)
ì            model: OpenAI model to use

        Returns:
            str: API response content
        """
        try:
            # Handle single image path
            if isinstance(image_path, str):
                image_paths = [image_path]
            else:
                image_paths = image_path

            # Prepare user message content
            user_content = [{"type": "text", "text": prompt}]

            # Add all images to the content
            for img_path in image_paths:
                base64_image = self.encode_image(img_path)
                user_content.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                })

            # Create messages array with system and user messages
            messages = [
                {
                    "role": "user",
                    "content": user_content
                }
            ]

            # Create API request
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
            )

            return response.choices[0].message.content

        except Exception as e:
            raise Exception(f"Error analyzing image(s): {str(e)}")


# Example usage
def main():
    # Initialize analyzer
    analyzer = LocalImageAnalyzer()

    try:
        # Example with a single image
        single_result = analyzer.analyze_image(
            image_path="path_to_single_image.jpg",
            user_prompt="Describe what you see in this image",
            system_prompt="You are an expert art critic. Analyze this image in detail."
        )
        print("Single Image Analysis:", single_result)

        # Example with multiple images
        multiple_result = analyzer.analyze_image(
            image_path=[
                "path_to_image1.jpg",
                "path_to_image2.jpg",
                "path_to_image3.jpg"
            ],
            user_prompt="Compare these images and describe their differences",
            system_prompt="You are a detail-oriented image comparison expert. Focus on subtle differences."
        )
        print("Multiple Images Analysis:", multiple_result)

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()