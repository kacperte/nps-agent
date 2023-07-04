"""

"""

from yoyo import step

__depends__ = {}

steps = [
    step(
        "CREATE TABLE sent_emails (email_id VARCHAR(255) NOT NULL, date TIMESTAMP WITH TIME ZONE NOT NULL, project VARCHAR(255) NOT NULL)",
        "DROP TABLE sent_emails",
    ),

    step(
        "CREATE TABLE opens (email_id VARCHAR(255) NOT NULL, date TIMESTAMP WITH TIME ZONE NOT NULL, project VARCHAR(255) NOT NULL)",
        "DROP TABLE opens",
    )
]
