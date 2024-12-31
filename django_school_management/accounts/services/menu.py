from django.urls import reverse
from django_school_management.accounts.models import User
from typing import List, Dict, Any, Set


class MenuService:
    def __init__(self, menu_config: Dict[str, Any]):
        """
        Initialize the MenuService with the given configuration.
        """
        self.menu_config = menu_config

    def get_user_groups(self, user: User) -> Set[str]:
        """
        Retrieve the groups of the user as a set.
        """
        return set(user.groups.values_list("name", flat=True))

    def add_urls_to_menu(
        self, menu_items: List[Dict[str, str]], urls: List[Dict[str, str]]
    ) -> None:
        """
        Add reversed URLs and titles to the menu_items list.
        """
        for url in urls:
            menu_items.append(
                {"url": reverse(url["name"]), "title": url["title"]}
            )

    def get_menu_items(self, section: str, user: User) -> List[Dict[str, str]]:
        """
        Retrieve menu items for a given section based on the user's groups.
        """
        user_groups = self.get_user_groups(user)
        menu_items = []

        if section not in self.menu_config:
            return menu_items

        for entry in self.menu_config[section]:
            if user_groups & entry["groups"]:
                self.add_urls_to_menu(menu_items, entry["urls"])

        return menu_items
