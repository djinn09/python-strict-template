# Vulture Whitelist for Example Template
# This file tells Vulture that these names are used, even if not explicitly called in the project.

import src.example

src.example.UserRole.ADMIN
src.example.UserRole.GUEST
src.example.Priority.LOW
src.example.Priority.HIGH
src.example.Priority.CRITICAL

src.example.User.id
src.example.User.name
src.example.User.email
src.example.User.created_at
src.example.User.name_must_not_be_empty

src.example.Task.id
src.example.Task.title
src.example.Task.description
src.example.Task.completed
src.example.Task.assignee_id

src.example.SafeCalculator.divide
src.example.SafeCalculator.safe_get

cls
