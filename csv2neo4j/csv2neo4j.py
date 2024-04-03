from neo4j import GraphDatabase
import csv
import json

with open('config.json') as f:
    cfg = json.load(f)


def check_node_exists(session, node_name, type):
    result = session.run("MATCH (n: `" + type + "`{name: $name}) RETURN COUNT(n) AS count", name=node_name)
    count = result.single()["count"]
    return count > 0


def check_relation_exists(session, start_node, end_node, relation):
    result = session.run(
        "MATCH (start)-[r:" + relation + "]->(end) WHERE start.name = $start_name AND end.name = $end_name RETURN COUNT(r) AS count",
        start_name=start_node, end_name=end_node)
    count = result.single()["count"]
    return count > 0


# Connect to Neo4j
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", cfg['password']))
with driver.session() as session:
    # 删除所有关系
    session.run("MATCH ()-[r]->() DELETE r")
    # 删除所有节点
    session.run("MATCH (n) DELETE n")
    for filename in cfg["filename_csv"]:
        with open(filename, 'r', encoding='utf-8') as file:
            # 创建CSV读取器
            data = csv.reader(file)
            next(data)
            for row in data:
                flag_of_relation = row[cfg['data/object']]
                subjectt = row[cfg['subject']]
                objectt = row[cfg['object']]
                relation = row[cfg['relation']]
                subjectt_type = row[cfg['subject_type']]
                objectt_type = row[cfg['object_type']]
                if not flag_of_relation and not check_node_exists(session, subjectt, subjectt_type):
                    session.run("CREATE (n:`" + subjectt_type + "` {name: $name })",
                                name=subjectt)

                if not check_node_exists(session, objectt, objectt_type):
                    session.run("CREATE (n:`" + objectt_type + "`{name: $name })",
                                name=objectt)
                if not flag_of_relation:
                    if subjectt != objectt and not check_relation_exists(session, subjectt, objectt, relation):
                        session.run(
                            "MATCH (start), (end) WHERE start.name = $start_name AND end.name = $end_name CREATE ("
                            "start)-[r:" + relation + "]->(end)",
                            start_name=objectt, end_name=subjectt)

                if flag_of_relation:
                    result = session.run("MATCH (n {name: $name}) "
                         "SET n.`" + relation + "` = COALESCE(n.`" + relation + "`, '') + CASE WHEN n.`" + relation + "` IS NULL THEN '' ELSE ';' END + $value ",
                         name=objectt, value=subjectt, relation=relation)
driver.close()
print("successfully")
