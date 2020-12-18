from dataclasses import dataclass
import enum


class ArtistRole(enum.Enum):
    Primary = "primary"
    Secondary = "secondary"
    Collaborator = "collaborator"
    Featured = "featured"


@dataclass
class Artist:
    role: ArtistRole = ArtistRole.Primary
    name: str = ''
