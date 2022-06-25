from loguru import logger
from tqdm import tqdm

from ChordNode import ChordNode

NUMBER_NODE = 6  # Количество узлов
BYTE_LENGTH = 5  # Количество бит в хеш-ключе


def stabilisation(nodes):
    """Стабилизация узлов в списке."""
    logger.info('Стабилизируем узлы...')

    for _ in tqdm(range(len(nodes) * len(nodes) + 1)):
        for node in nodes:
            node.stabilize()
            node.fix_fingers()

    logger.info('Стабилизация окончена')

    for node in nodes:
        logger.debug(f'{str(node)}')


if __name__ == '__main__':
    node_list = []
    head_node = ChordNode(0, BYTE_LENGTH)
    head_node.join(None)
    node_list.append(head_node)

    for n in range(1, NUMBER_NODE + 1):
        chord_node = ChordNode(n, BYTE_LENGTH)
        chord_node.join_to_node(head_node)
        node_list.append(chord_node)

    logger.info('Узлы созданы')
    stabilisation(node_list)

    logger.info('Добавим узел...')
    new_node = ChordNode(9, BYTE_LENGTH)
    new_node.join_to_node(head_node)
    node_list.append(new_node)
    stabilisation(node_list)
    logger.info('Узел добавлен')

    logger.info('Добавим узел...')
    new_node = ChordNode(13, BYTE_LENGTH)
    new_node.join_to_node(head_node)
    node_list.append(new_node)
    stabilisation(node_list)
    logger.info('Узел добавлен')

    logger.info('Добавим узел...')
    new_node = ChordNode(15, BYTE_LENGTH)
    new_node.join_to_node(head_node)
    node_list.append(new_node)
    stabilisation(node_list)
    logger.info('Узел добавлен')

    logger.info('Удаляем добавленный узел...')
    node_list.remove(new_node)
    new_node.remove()
    stabilisation(node_list)
    logger.info('Узел удален успешно')
