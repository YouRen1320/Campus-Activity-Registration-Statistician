#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
校园活动报名统计器
功能：统计社团招新活动的报名数据
"""

import csv
from collections import defaultdict, Counter
from datetime import datetime
import os
import sys

class RegistrationAnalyzer:
    """校园活动报名统计器类"""
    
    def __init__(self):
        """初始化报名数据和统计结果"""
        self.registrations = []
        self.college_stats = {}
        self.gender_stats = {'男': 0, '女': 0}
        self.time_stats = {}
        
    def load_data_from_csv(self, filename):
        """从CSV文件加载报名数据"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.registrations.append(row)
            return True
        except Exception as e:
            print(f"加载数据时出错: {e}")
            return False
    
    def input_data_manually(self):
        """手动输入报名数据"""
        print("请输入报名数据（输入'完成'结束）：")
        print("格式：姓名,性别,学院,报名时间（如：张三,男,信息学院,19:30）")
        
        while True:
            data = input("> ")
            if data == '完成':
                break
                
            try:
                name, gender, college, reg_time = data.split(',')
                self.registrations.append({
                    '姓名': name.strip(),
                    '性别': gender.strip(),
                    '学院': college.strip(),
                    '报名时间': reg_time.strip()
                })
            except ValueError:
                print("输入格式不正确，请重试")
        
    def analyze_data(self):
        """分析报名数据"""
        if not self.registrations:
            print("没有报名数据可分析")
            return False
            
        # 去除重复报名
        unique_registrations = []
        seen_names = set()
        for reg in self.registrations:
            if reg['姓名'] not in seen_names:
                unique_registrations.append(reg)
                seen_names.add(reg['姓名'])
        
        self.registrations = unique_registrations
        total_registrations = len(self.registrations)
        
        # 统计各学院人数占比
        college_counter = Counter()
        for reg in self.registrations:
            college = reg.get('学院', '未知')
            college_counter[college] += 1
        
        self.college_stats = {college: {
            'count': count,
            'percentage': round(count / total_registrations * 100, 2)
        } for college, count in college_counter.items()}
        
        # 重置性别统计数据
        self.gender_stats = {'男': 0, '女': 0}
        
        # 按性别分类统计
        for reg in self.registrations:
            gender = reg.get('性别', '未知')
            if gender in ['男', '女']:
                self.gender_stats[gender] += 1
            
        # 分析报名时间
        time_counter = Counter()
        for reg in self.registrations:
            time_str = reg.get('报名时间', '')
            if time_str:
                # 将时间转换为小时段
                try:
                    hour = time_str.split(':')[0]
                    time_period = f"{hour}:00-{hour}:59"
                    time_counter[time_period] += 1
                except:
                    pass
        
        # 获取报名人数最多的三个时间段
        self.time_stats = dict(time_counter.most_common(3))
        
        return True
                
    def generate_report(self):
        """生成报名统计报告"""
        if not hasattr(self, 'college_stats') or not self.college_stats:
            print("请先分析数据")
            return
            
        report = []
        report.append("=" * 50)
        report.append("校园活动报名统计报告")
        report.append("=" * 50)
        report.append(f"总报名人数: {len(self.registrations)}人")
        report.append("\n各学院报名情况:")
        
        for college, stats in self.college_stats.items():
            report.append(f"- {college}: {stats['count']}人 (占比{stats['percentage']}%)")
        
        report.append("\n性别分布:")
        report.append(f"- 男生: {self.gender_stats['男']}人")
        report.append(f"- 女生: {self.gender_stats['女']}人")
        
        report.append("\n报名高峰时段 (TOP3):")
        for time_period, count in self.time_stats.items():
            report.append(f"- {time_period}: {count}人")
            
        report.append("\n简要分析:")
        # 找出报名人数最多的学院
        top_college = max(self.college_stats.items(), key=lambda x: x[1]['count'])[0]
        report.append(f"1. {top_college}的学生参与度最高，建议重点关注该学院的需求和反馈。")
        
        # 性别比例分析
        male_percentage = round(self.gender_stats['男'] / len(self.registrations) * 100, 2)
        female_percentage = round(self.gender_stats['女'] / len(self.registrations) * 100, 2)
        if male_percentage > female_percentage:
            report.append(f"2. 男生参与比例({male_percentage}%)高于女生({female_percentage}%)，可考虑增加对女生的吸引力。")
        else:
            report.append(f"2. 女生参与比例({female_percentage}%)高于男生({male_percentage}%)，可考虑增加对男生的吸引力。")
        
        # 时间分析
        if self.time_stats:
            peak_time = list(self.time_stats.keys())[0]
            report.append(f"3. 报名高峰集中在{peak_time}时段，建议在该时段安排更多工作人员。")
        
        report.append("=" * 50)
        
        return "\n".join(report)
    
    def save_report(self, report, filename="报名统计报告.txt"):
        """保存报告到文件"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"报告已保存到 {filename}")
            return True
        except Exception as e:
            print(f"保存报告时出错: {e}")
            return False
    
    def privacy_protection_analysis(self):
        """个人信息隐私保护方法分析"""
        analysis = []
        analysis.append("=" * 50)
        analysis.append("报名数据中个人信息的隐私保护方法分析")
        analysis.append("=" * 50)
        
        analysis.append("1. 数据收集原则")
        analysis.append("   - 最小化原则：只收集必要的个人信息，如不需要具体姓名可使用匿名ID")
        analysis.append("   - 告知同意原则：明确告知用户数据用途并获取同意")
        
        analysis.append("\n2. 数据存储安全")
        analysis.append("   - 加密存储：使用加密算法保护存储的个人数据")
        analysis.append("   - 访问控制：严格限制数据访问权限，只允许授权人员访问")
        analysis.append("   - 定期清理：活动结束后及时删除不再需要的个人信息")
        
        analysis.append("\n3. 数据匿名化技术")
        analysis.append("   - 数据脱敏：将敏感信息（如姓名）替换为随机ID")
        analysis.append("   - 数据聚合：使用统计结果代替原始数据进行分析")
        analysis.append("   - K-匿名性：确保无法通过数据组合识别特定个人")
        
        analysis.append("\n4. 系统实现建议")
        analysis.append("   - 在当前系统中，可以实现以下改进：")
        analysis.append("     a. 报告生成阶段对原始数据进行脱敏处理")
        analysis.append("     b. 实现数据访问日志，记录谁在何时访问了数据")
        analysis.append("     c. 设置数据自动过期机制，活动结束后自动删除原始数据")
        
        analysis.append("\n5. 法律法规合规")
        analysis.append("   - 遵守《个人信息保护法》等相关法律")
        analysis.append("   - 建立个人信息保护责任制度和应急响应机制")
        
        analysis.append("=" * 50)
        
        return "\n".join(analysis)

def generate_sample_data(filename="sample_data.csv"):
    """生成示例数据用于测试"""
    colleges = ["信息学院", "文传学院", "经管学院", "理学院", "外语学院"]
    genders = ["男", "女"]
    
    # 生成随机报名时间
    times = ["08:30", "09:15", "10:45", "12:30", "14:00", 
             "15:30", "16:45", "18:20", "19:00", "19:30", 
             "20:00", "20:15", "20:30"]
    
    # 生成示例姓名
    male_names = ["张三", "李四", "王五", "赵六", "钱七", "孙八", 
                 "周九", "吴十", "郑十一", "王明", "李华", "张伟", 
                 "刘强", "陈晨", "杨光", "赵阳", "钱峰", "孙林", 
                 "周涛", "吴刚", "郑达", "冯云", "陈亮", "朱峰"]
    
    female_names = ["张丽", "李娜", "王芳", "赵静", "钱红", "孙雪", 
                   "周梅", "吴兰", "郑霞", "王颖", "李玲", "张婷", 
                   "刘洁", "陈蓉", "杨燕", "赵敏", "钱莉", "孙艳", 
                   "周琳", "吴英", "郑丽", "冯洁", "陈婷", "朱玲"]
    
    import random
    
    # 准备数据
    headers = ["姓名", "性别", "学院", "报名时间"]
    rows = []
    
    # 生成80条记录
    for i in range(80):
        gender = random.choice(genders)
        if gender == "男":
            name = random.choice(male_names)
        else:
            name = random.choice(female_names)
            
        college = random.choice(colleges)
        time = random.choice(times)
        
        rows.append([name, gender, college, time])
    
    # 故意添加一些重复数据以测试去重功能
    for _ in range(5):
        rows.append(random.choice(rows))
    
    # 写入CSV文件
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)
        print(f"示例数据已生成到 {filename}")
        return True
    except Exception as e:
        print(f"生成示例数据时出错: {e}")
        return False

def main():
    """主函数"""
    print("=" * 50)
    print("校园活动报名统计器")
    print("=" * 50)
    
    analyzer = RegistrationAnalyzer()
    
    while True:
        print("\n请选择操作：")
        print("1. 生成示例数据")
        print("2. 从CSV文件加载数据")
        print("3. 手动输入数据")
        print("4. 分析数据")
        print("5. 生成并显示报告")
        print("6. 保存报告到文件")
        print("7. 查看个人信息隐私保护分析")
        print("0. 退出程序")
        
        choice = input("请输入选项编号: ")
        
        if choice == '1':
            generate_sample_data()
        elif choice == '2':
            filename = input("请输入CSV文件路径: ")
            if analyzer.load_data_from_csv(filename):
                print(f"成功从 {filename} 加载了 {len(analyzer.registrations)} 条数据")
        elif choice == '3':
            analyzer.input_data_manually()
            print(f"已输入 {len(analyzer.registrations)} 条数据")
        elif choice == '4':
            if analyzer.analyze_data():
                print("数据分析完成")
        elif choice == '5':
            report = analyzer.generate_report()
            if report:
                print("\n" + report)
        elif choice == '6':
            report = analyzer.generate_report()
            if report:
                filename = input("请输入保存报告的文件名 (默认为'报名统计报告.txt'): ")
                if not filename:
                    filename = "报名统计报告.txt"
                analyzer.save_report(report, filename)
        elif choice == '7':
            privacy_analysis = analyzer.privacy_protection_analysis()
            print("\n" + privacy_analysis)
        elif choice == '0':
            print("感谢使用，再见！")
            break
        else:
            print("无效选项，请重新选择")

if __name__ == "__main__":
    main() 