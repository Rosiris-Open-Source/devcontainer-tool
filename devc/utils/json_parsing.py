# Copyright 2025 Manuel Muth
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Helper functions used for parsing .json files."""
from collections.abc import Iterable


def filter_empty_strings(value: Iterable[str]) -> list[str]:
    r"""
    Filter out empty or non-renderable strings from an iterable.

    This removes strings that are empty or contain only whitespace characters,
    such as '', '\n', or '\t'.

    Args:
        value: An iterable of strings, or None.

    Returns
    -------
    List[str]: A list containing only non-empty strings.

    """
    if not value:
        return []
    return [v for v in value if v.strip()]
