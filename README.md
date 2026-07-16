# DeliveryAutoChecker 产品交付自动化质检工具
适配安防行业产品交付场景，模拟企业交付中心完整工作流，用于交付资料校验、故障工单管理、自动化运维、AI智能文本审核，匹配大华交付工程师技术栈要求。

## 项目背景
传统产品交付依赖人工核对海量交付文档、手动统计设备故障工单，效率低、易遗漏。本工具实现全流程自动化，减少人工操作，同步产出质量分析报表，辅助推动产品优化迭代。

## 技术栈
Python3 | Shell | Perl | MySQL | Linux(CentOS) | 轻量AI文本接口

## 核心功能
1. 交付文档自动化校验
批量扫描交付技术文档，自动检测缺失字段、参数格式错误，生成标准化校验报告。
2. Linux自动化运维脚本
提供一键部署、定时巡检、日志故障抓取脚本，适配企业服务器运维场景。
3. ITR故障工单数据管理
MySQL存储所有交付故障工单，内置多维度统计SQL，自动分析高频产品问题，输出优化依据。
4. AI智能文本校验模块
接入开源大模型接口，智能识别文档不规范描述，对标企业AI交付机器人研发需求。
5. 多语言脚本支撑
配套Perl日志处理脚本，覆盖岗位招聘偏好技术。

## 部署教程（CentOS Linux）
1. 克隆仓库
git clone https://github.com/你的ID/DeliveryAutoChecker.git
2. 执行一键部署脚本
chmod +x shell_script/auto_deploy.sh
./shell_script/auto_deploy.sh
3. 初始化数据库
mysql -uroot -p < sql/create_table.sql
4. 运行文档校验工具
python3 python_core/doc_checker.py
