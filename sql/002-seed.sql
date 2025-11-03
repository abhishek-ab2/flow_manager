INSERT INTO tasks (task_name, impl_path) VALUES ('task1', 'app.tasks.task1:Fetch') ON DUPLICATE KEY UPDATE impl_path=VALUES(impl_path);
INSERT INTO tasks (task_name, impl_path) VALUES ('task2', 'app.tasks.task2:Process') ON DUPLICATE KEY UPDATE impl_path=VALUES(impl_path);
INSERT INTO tasks (task_name, impl_path) VALUES ('task3', 'app.tasks.task3:Store') ON DUPLICATE KEY UPDATE impl_path=VALUES(impl_path);
