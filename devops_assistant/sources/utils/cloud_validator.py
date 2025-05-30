class CloudValidator:
    def validate_provider(self, provider: str) -> bool:
        # TODO: Implement actual validation against supported providers
        supported = ["aws", "gcp", "azure"]
        return provider.lower() in supported

    def validate_region(self, provider: str, region: str) -> bool:
        # TODO: Implement region checks
        return True