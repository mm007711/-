#!/usr/bin/env python3
"""
添加更多题目到数据库
"""

import sqlite3
import datetime

def add_problems():
    print("添加更多题目到数据库...")
    
    conn = sqlite3.connect('codeedu.db')
    cursor = conn.cursor()
    
    # 检查当前题目数量
    cursor.execute("SELECT COUNT(*) FROM problems")
    current_count = cursor.fetchone()[0]
    print(f"当前题目数量: {current_count}")
    
    # 新题目数据
    new_problems = [
        {
            'title': '反转字符串',
            'description': '编写一个函数，将输入的字符串反转过来。\n\n示例 1:\n输入: "hello"\n输出: "olleh"\n\n示例 2:\n输入: "A man, a plan, a canal: Panama"\n输出: "amanaP :lanac a ,nalp a ,nam A"',
            'difficulty': 'easy',
            'score': 10,
            'time_limit': 1000,
            'memory_limit': 256,
            'tags': '字符串,基础',
            'is_public': True
        },
        {
            'title': '有效的括号',
            'description': '给定一个只包括 \'(\', \')\', \'{\', \'}\', \'[\', \']\' 的字符串 s ，判断字符串是否有效。\n\n有效字符串需满足：\n1. 左括号必须用相同类型的右括号闭合。\n2. 左括号必须以正确的顺序闭合。\n3. 每个右括号都有一个对应的相同类型的左括号。',
            'difficulty': 'easy',
            'score': 10,
            'time_limit': 1000,
            'memory_limit': 256,
            'tags': '栈,字符串',
            'is_public': True
        },
        {
            'title': '合并两个有序链表',
            'description': '将两个升序链表合并为一个新的 升序 链表并返回。新链表是通过拼接给定的两个链表的所有节点组成的。',
            'difficulty': 'easy',
            'score': 15,
            'time_limit': 1000,
            'memory_limit': 256,
            'tags': '链表,递归',
            'is_public': True
        },
        {
            'title': '最长回文子串',
            'description': '给你一个字符串 s，找到 s 中最长的回文子串。\n\n示例 1:\n输入: s = "babad"\n输出: "bab"\n解释: "aba" 同样是符合题意的答案。',
            'difficulty': 'medium',
            'score': 20,
            'time_limit': 2000,
            'memory_limit': 512,
            'tags': '字符串,动态规划',
            'is_public': True
        },
        {
            'title': '三数之和',
            'description': '给你一个整数数组 nums ，判断是否存在三元组 [nums[i], nums[j], nums[k]] 满足 i != j、i != k 且 j != k ，同时还满足 nums[i] + nums[j] + nums[k] == 0 。请你返回所有和为 0 且不重复的三元组。',
            'difficulty': 'medium',
            'score': 25,
            'time_limit': 3000,
            'memory_limit': 512,
            'tags': '数组,双指针',
            'is_public': True
        },
        {
            'title': '正则表达式匹配',
            'description': '给你一个字符串 s 和一个字符规律 p，请你来实现一个支持 \'.\' 和 \'*\' 的正则表达式匹配。\n\n- \'.\' 匹配任意单个字符\n- \'*\' 匹配零个或多个前面的那一个元素\n\n所谓匹配，是要涵盖 整个 字符串 s 的，而不是部分字符串。',
            'difficulty': 'hard',
            'score': 30,
            'time_limit': 5000,
            'memory_limit': 1024,
            'tags': '字符串,动态规划',
            'is_public': True
        },
        {
            'title': '合并K个升序链表',
            'description': '给你一个链表数组，每个链表都已经按升序排列。\n\n请你将所有链表合并到一个升序链表中，返回合并后的链表。',
            'difficulty': 'hard',
            'score': 30,
            'time_limit': 5000,
            'memory_limit': 1024,
            'tags': '链表,堆',
            'is_public': True
        },
        {
            'title': '二叉树的最大深度',
            'description': '给定一个二叉树 root ，返回其最大深度。\n\n二叉树的 最大深度 是指从根节点到最远叶子节点的最长路径上的节点数。',
            'difficulty': 'easy',
            'score': 10,
            'time_limit': 1000,
            'memory_limit': 256,
            'tags': '树,深度优先搜索',
            'is_public': True
        },
        {
            'title': '对称二叉树',
            'description': '给你一个二叉树的根节点 root ， 检查它是否轴对称。',
            'difficulty': 'easy',
            'score': 10,
            'time_limit': 1000,
            'memory_limit': 256,
            'tags': '树,深度优先搜索',
            'is_public': True
        },
        {
            'title': '二叉树的层序遍历',
            'description': '给你二叉树的根节点 root ，返回其节点值的 层序遍历 。 （即逐层地，从左到右访问所有节点）。',
            'difficulty': 'medium',
            'score': 15,
            'time_limit': 2000,
            'memory_limit': 512,
            'tags': '树,广度优先搜索',
            'is_public': True
        }
    ]
    
    # 添加新题目
    created_by = 2  # test_teacher的用户ID
    created_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    for problem in new_problems:
        cursor.execute('''
            INSERT INTO problems 
            (title, description, difficulty, score, time_limit, memory_limit, tags, created_by, created_at, is_public)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            problem['title'],
            problem['description'],
            problem['difficulty'],
            problem['score'],
            problem['time_limit'],
            problem['memory_limit'],
            problem['tags'],
            created_by,
            created_at,
            problem['is_public']
        ))
    
    conn.commit()
    
    # 检查添加后的题目数量
    cursor.execute("SELECT COUNT(*) FROM problems")
    new_count = cursor.fetchone()[0]
    print(f"添加后题目数量: {new_count}")
    print(f"成功添加了 {new_count - current_count} 个新题目")
    
    # 显示新添加的题目
    print("\n新添加的题目:")
    cursor.execute("SELECT id, title, difficulty FROM problems ORDER BY id DESC LIMIT 10")
    new_problems_list = cursor.fetchall()
    
    for prob in new_problems_list:
        print(f"  ID: {prob[0]}, 标题: {prob[1]}, 难度: {prob[2]}")
    
    conn.close()
    
    print("\n✅ 题目添加完成！")

if __name__ == "__main__":
    add_problems()
