CREATE TABLE flows (
    id VARCHAR(255) NOT NULL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    payload JSON NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE flow_runs (
    id VARCHAR(255) NOT NULL PRIMARY KEY,
    flow_id VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL,
    started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    finished_at DATETIME NULL,
    INDEX idx_flow_runs_flow_id (flow_id),
    CONSTRAINT fk_flow_runs_flow
        FOREIGN KEY (flow_id) REFERENCES flows(id)
        ON DELETE CASCADE
);

CREATE TABLE task_runs (
    id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    run_id VARCHAR(255) NOT NULL,
    task_name VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL,
    output TEXT NULL,
    error TEXT NULL,
    started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    finished_at DATETIME NULL,
    INDEX idx_task_runs_run_id (run_id)
);

CREATE TABLE tasks (
    id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    task_name VARCHAR(255) NOT NULL UNIQUE,
    impl_path VARCHAR(512) NOT NULL
);
