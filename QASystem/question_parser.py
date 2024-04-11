class QuestionPaser:

    '''构建实体节点'''
    def build_entitydict(self, args):
        entity_dict = {}
        for arg, types in args.items():
            for type in types:
                if type not in entity_dict:
                    entity_dict[type] = [arg]
                else:
                    entity_dict[type].append(arg)

        return entity_dict

    '''解析主函数'''
    def parser_main(self, res_classify):
        args = res_classify['args']
        entity_dict = self.build_entitydict(args)
        question_types = res_classify['question_types']
        sqls = []
        for question_type in question_types:
            sql_ = {}
            sql_['question_type'] = question_type
            sql = []
            sql = self.sql_transfer(question_type, args)
            if sql:
                sql_['sql'] = sql

                sqls.append(sql_)

        return sqls

    '''针对不同的问题，分开进行处理'''
    def sql_transfer(self, question_type, entities):
        if not entities:
            return []

        # 查询语句
        sql = []
        # print('你所询问的类型是：', question_type)
        # 查询包含关系
        if question_type == 'contain':
            sql = ["MATCH (m)-[r:包含]->(n) where m.name = '{0}' return m.name, n.name".format(i) for i in entities]

        # 查询等价关系
        elif question_type == 'equal':
            sql1 = ["MATCH (m)-[r:等价]->(n) where m.name = '{0}' return m.name, n.name".format(i) for i in entities]
            sql2 = ["MATCH (n)-[r:等价]->(m) where m.name = '{0}' return m.name, n.name".format(i) for i in entities]
            sql = sql1 + sql2

        # 查询来源关系
        elif question_type == 'derive':
            sql = ["MATCH (m)-[r:来源]->(n) where m.name = '{0}' return m.name, n.name".format(i) for i in entities]

        # 查询属于关系
        elif question_type == 'belong':
            sql = ["MATCH (m)-[r:属于]->(n) where m.name = '{0}' return m.name, n.name".format(i) for i in entities]

        # 查询由组成关系
        elif question_type == 'compose':
            sql = ["MATCH (m)-[r:由组成]->(n) where m.name = '{0}' return m.name, n.name".format(i) for i in entities]
        
        # 查询习题关系
        elif question_type == 'exercise':
            sql = ["MATCH (m)-[r:习题]->(n) where m.name = '{0}' return m.name, n.name".format(i) for i in entities]        

        # 查询某名词的实现手段
        elif question_type == 'realize':
            sql = ["MATCH (m)-[r:实现]->(n) where m.name = '{0}' return m.name, n.name".format(i) for i in entities]

        # 查询某名词的定义
        elif question_type == 'define':
           sql = ["MATCH (m) where m.name = '{0}' and exists(m.被定义为) return m.name, m.被定义为".format(i) for i in entities]

        # 查询某名词的内容是什么
        elif question_type == 'content':
            sql = ["MATCH (m) where m.name = '{0}' return m.name, m.内容".format(i) for i in entities]

        # 查询某名词的英文名称
        elif question_type == 'engname':
            sql = ["MATCH (m) where m.name = '{0}' return m.name, m.英文名".format(i) for i in entities]

        # 查询某名词的创建的目的
        elif question_type == 'target':
            sql = ["MATCH (m) where m.name = '{0}' return m.name, m.目标".format(i) for i in entities]

        # 查询某名词的作用
        elif question_type == 'effect':
            sql = ["MATCH (m) where m.name = '{0}' return m.name, m.作用".format(i) for i in entities]

        # 查询某名词的特点
        elif question_type == 'character':
            sql = ["MATCH (m) where m.name = '{0}' return m.name, m.特点".format(i) for i in entities]

        # 查询某名词的方法
        elif question_type == 'method':
            sql = ["MATCH (m) where m.name = '{0}' return m.name, m.方法".format(i) for i in entities]

        # 查询某名词的缺点
        elif question_type == 'flaw':
            sql = ["MATCH (m) where m.name = '{0}' return m.name, m.缺点".format(i) for i in entities]

        # 查询某名词的创建时间
        elif question_type == 'create_time':
            sql = ["MATCH (m) where m.name = '{0}' return m.name, m.创建时间".format(i) for i in entities]

        # 查询某名词的创建者
        elif question_type == 'creator':
            sql = ["MATCH (m) where m.name = '{0}' return m.name, m.创建者".format(i) for i in entities]
        
        # 查询某名词的链接
        elif question_type == 'link':
            sql = ["MATCH (m) where m.name = '{0}' return m.name, m.链接".format(i) for i in entities]

        return sql



if __name__ == '__main__':
    handler = QuestionPaser()
