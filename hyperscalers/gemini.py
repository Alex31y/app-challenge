import google.generativeai as genai
import PIL.Image
from typing import Optional, List, Union, Tuple, Dict


class GeminiImageAnalyzer:
    def __init__(self, api_key: str):
        """
        Initialize the Gemini Image Analyzer.

        Args:
            api_key: Your Google API key for Gemini
        """
        try:
            genai.configure(api_key=api_key)
            # Default to Gemini 1.5 Pro as it handles images well
            self.model = genai.GenerativeModel("gemini-exp-1121")
        except Exception as e:
            raise Exception(f"Error initializing Gemini API: {str(e)}")

    def load_image(self, image_path: str) -> PIL.Image.Image:
        """
        Load an image file using PIL.

        Args:
            image_path: Path to the local image file

        Returns:
            PIL.Image.Image: Loaded image object
        """
        try:
            return PIL.Image.open(image_path)
        except Exception as e:
            raise Exception(f"Error loading image file: {str(e)}")

    def analyze_image(
            self,
            image_path: Union[str, List[str]],
            prompt: str = "What's in this image?",
            model: str = "gemini-exp-1121",
            max_tokens: Optional[int] = None
    ) -> Tuple[str, Dict[str, int]]:
        """
        Analyze one or more local images using Gemini API.

        Args:
            image_path: Path to local image file or list of paths for multiple images
            prompt: Question or prompt about the image(s)
            model: Gemini model to use (default: gemini-1.5-pro)
            max_tokens: Maximum tokens in response (optional)

        Returns:
            tuple: (API response content, token usage dictionary)
        """
        try:
            # Update model if different from default
            if model != self.model.model_name:
                self.model = genai.GenerativeModel(model)

            # Handle single image or multiple images
            if isinstance(image_path, str):
                image_list = [self.load_image(image_path)]
            else:
                image_list = [self.load_image(img_path) for img_path in image_path]

            # Prepare content list
            contents = [*image_list, "\n\n", prompt]

            # Get input token count
            input_tokens = self.model.count_tokens(contents)

            # Create generation config if max_tokens specified
            generation_config = None
            if max_tokens:
                generation_config = genai.types.GenerationConfig(
                    max_output_tokens=max_tokens
                )

            # Generate content with images and prompt
            response = self.model.generate_content(
                contents=contents,
                generation_config=generation_config
            )

            # Get token usage from response metadata
            token_usage = {
                "input_tokens": response.usage_metadata.prompt_token_count,
                "output_tokens": response.usage_metadata.candidates_token_count,
                "total_tokens": response.usage_metadata.total_token_count
            }

            return response.text, token_usage

        except Exception as e:
            raise Exception(f"Error analyzing image: {str(e)}")
