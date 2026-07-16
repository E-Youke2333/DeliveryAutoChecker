-- ITR故障工单表
CREATE DATABASE IF NOT EXISTS delivery_quality;
USE delivery_quality;

DROP TABLE IF EXISTS fault_ticket;
CREATE TABLE fault_ticket(
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '工单ID',
    device_model VARCHAR(100) COMMENT '设备型号',
    fault_desc TEXT COMMENT '故障描述',
    deliver_date DATE COMMENT '交付日期',
    status TINYINT COMMENT '0未解决 1已闭环',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 交付文档校验日志表
DROP TABLE IF EXISTS doc_check_log;
CREATE TABLE doc_check_log(
    log_id INT PRIMARY KEY AUTO_INCREMENT,
    file_name VARCHAR(200),
    error_count INT,
    check_time DATETIME DEFAULT CURRENT_TIMESTAMP
);

