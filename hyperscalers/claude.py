import base64
import mimetypes
from typing import Optional, Dict, List, Union, Tuple
from anthropic import Anthropic


class ClaudeImageAnalyzer:
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Claude Image Analyzer.

        Args:
            api_key: Your Anthropic API key (optional if set in environment)
        """
        try:
            self.client = Anthropic(api_key=api_key)
            self.default_model = "claude-3-5-sonnet-20241022"
        except Exception as e:
            raise Exception(f"Error initializing Anthropic API: {str(e)}")

    def _get_media_type(self, image_path: str) -> str:
        """
        Get the MIME type of the image file.

        Args:
            image_path: Path to the image file

        Returns:
            str: MIME type of the image
        """
        mime_type, _ = mimetypes.guess_type(image_path)
        if not mime_type or not mime_type.startswith('image/'):
            raise ValueError(f"Unsupported file type: {image_path}")
        return mime_type

    def _encode_image(self, image_path: str) -> tuple[str, str]:
        """
        Read and encode image file to base64.

        Args:
            image_path: Path to the image file

        Returns:
            tuple: (media_type, base64_encoded_data)
        """
        try:
            media_type = self._get_media_type(image_path)
            with open(image_path, "rb") as image_file:
                encoded_data = base64.b64encode(image_file.read()).decode('utf-8')
            return media_type, encoded_data
        except Exception as e:
            raise Exception(f"Error processing image file: {str(e)}")

    def analyze_image(
            self,
            image_paths: Union[str, List[str]],
            prompt: str = "Describe this image.",
            system_prompt: Optional[str] = None,
            model: Optional[str] = None,
            max_tokens: int = 1024,
            temperature: float = 1.0,
            additional_params: Optional[Dict] = None
    ) -> Tuple[str, Dict[str, int]]:
        """
        Analyze one or more images using Claude API.

        Args:
            image_paths: Path or list of paths to image files
            prompt: Question or prompt about the image(s)
            system_prompt: System prompt to guide Claude's behavior
            model: Claude model to use (default: claude-3-sonnet)
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature (0-1)
            additional_params: Additional API parameters

        Returns:
            tuple: (API response content, token usage dictionary)
        """
        try:
            # Handle single image or list of images
            if isinstance(image_paths, str):
                image_paths = [image_paths]

            # Prepare message content
            content = []

            # Add images with descriptive text for each
            for idx, image_path in enumerate(image_paths, 1):
                # Add image number text
                if len(image_paths) > 1:
                    content.append({
                        "type": "text",
                        "text": f"Image {idx}:"
                    })

                # Add image
                media_type, image_data = self._encode_image(image_path)
                content.append({
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": media_type,
                        "data": image_data,
                    }
                })

            # Add the final prompt text
            content.append({
                "type": "text",
                "text": prompt
            })

            # Prepare API parameters
            api_params = {
                "model": model or self.default_model,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "messages": [
                    {
                        "role": "user",
                        "content": content
                    }
                ]
            }

            # Add system prompt if provided
            if system_prompt:
                api_params["system"] = system_prompt

            # Add any additional parameters
            if additional_params:
                api_params.update(additional_params)

            # Make API call
            response = self.client.messages.create(**api_params)

            # Extract token usage
            token_usage = {
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens,
                "total_tokens": response.usage.input_tokens + response.usage.output_tokens
            }

            return response.content[0].text, token_usage

        except Exception as e:
            raise Exception(f"Error analyzing image: {str(e)}")

    def analyze_images_conversation(
            self,
            messages: List[Dict],
            model: Optional[str] = None,
            max_tokens: int = 1024,
            temperature: float = 1.0,
            system_prompt: Optional[str] = None
    ) -> Tuple[str, Dict[str, int]]:
        """
        Have a conversation about images with Claude, maintaining context.

        Args:
            messages: List of message dictionaries with roles and content
            model: Claude model to use
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature
            system_prompt: System prompt to guide Claude's behavior

        Returns:
            tuple: (API response content, token usage dictionary)
        """
        try:
            api_params = {
                "model": model or self.default_model,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "messages": messages
            }

            if system_prompt:
                api_params["system"] = system_prompt

            response = self.client.messages.create(**api_params)

            token_usage = {
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens,
                "total_tokens": response.usage.input_tokens + response.usage.output_tokens
            }

            return response.content[0].text, token_usage

        except Exception as e:
            raise Exception(f"Error in conversation: {str(e)}")