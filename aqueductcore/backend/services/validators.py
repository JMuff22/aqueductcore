"""Validator functions to validate different inputs and parameters"""
from typing import List, Optional

from aqueductcore.backend.server.errors import ECSValidationError
from aqueductcore.backend.services.utils import is_tag_valid
from aqueductcore.backend.services.constants import (
    MAX_EXPERIMENT_TITLE_LENGTH,
    MAX_EXPERIMENT_DESCRIPTION_LENGTH,
    MAX_TAG_LENGTH,
    MAX_EXPERIMENT_TAGS,
    MAX_FILTER_TITLE_LENGTH,
    MAX_SHOULD_INCLUDE_TAGS_LENGTH,
    MAX_TAGS_ALLOWED_IN_FILTER
)


def validate_title(title: str):
    """Validate title to have a specified maximum length"""
    if title and len(title) > MAX_EXPERIMENT_TITLE_LENGTH:
        raise ECSValidationError(
            f"Title should be maximum {MAX_EXPERIMENT_TITLE_LENGTH} characters long."
        )

def validate_description(description: str):
    """Validate description to have a specified maximum length"""
    if description and len(description) > MAX_EXPERIMENT_DESCRIPTION_LENGTH:
        raise ECSValidationError(
            f"Description should be maximum {MAX_EXPERIMENT_DESCRIPTION_LENGTH} characters long."
        )

def validate_tags(tags: List[str]):
    """Check if only specified number of tags are present in the request"""
    if tags:
        if len(tags) > MAX_EXPERIMENT_TAGS:
            raise ECSValidationError(
                f"You can have a maximum of {MAX_EXPERIMENT_TAGS} tags in an experiment."
            )
        invalid_tags = [tag for tag in tags if len(tag) > MAX_TAG_LENGTH or not is_tag_valid(tag)]
        if invalid_tags:
            raise ECSValidationError(f"Tags {invalid_tags} are invalid.")

def validate_experiment_filters(
        title: Optional[str] = None,
        tags: Optional[List[str]] = None,
        should_include_tags: Optional[List[str]] = None
    ):
    """Validate filters received in request"""
    if title and len(title) > MAX_FILTER_TITLE_LENGTH:
        raise ECSValidationError(
            f"Title should be maximum {MAX_FILTER_TITLE_LENGTH} characters long."
        )

    if tags:
        if len(tags) > MAX_TAGS_ALLOWED_IN_FILTER:
            raise ECSValidationError(
                f"You can filter for maximum of {MAX_TAGS_ALLOWED_IN_FILTER} tags at a time."
            )

        invalid_tags = [tag for tag in tags if len(tag) > MAX_TAG_LENGTH or not is_tag_valid(tag)]
        if invalid_tags:
            raise ECSValidationError(f"Tags {invalid_tags} are invalid.")

    if should_include_tags:
        if len(should_include_tags) > MAX_SHOULD_INCLUDE_TAGS_LENGTH:
            raise ECSValidationError(
                f"You can filter for maximum of {MAX_SHOULD_INCLUDE_TAGS_LENGTH} tags " + \
                    "in should_include_tags at a time."
            )
        invalid_tags = [tag for tag in should_include_tags if len(tag) > MAX_TAG_LENGTH
                        or not is_tag_valid(tag)]
        if invalid_tags:
            raise ECSValidationError(f"Tags {invalid_tags} are invalid in " + \
                                " shouldIncludeTags filter.")

def validate_tag(tag: str):
    """Validate tag to have a specified maximum length and allowed characters only"""
    if len(tag) > MAX_TAG_LENGTH or not is_tag_valid(tag):
        raise ECSValidationError(f"Tag should be less than {MAX_TAG_LENGTH} characters long " + \
                            "and contain alphanumeric characters, hyphens and underscores only.")
