 stmt = text("SELECT ListID FROM {} ORDER BY ListID DESC LIMIT 1".format(table))
        select_last_list_id = connect.execute(stmt)
        last_list_id = select_last_list_id.fetchone()[0]
        prefix, _ = last_list_id.split('-')
        incremented_prefix = copy.copy(prefix)
        incrementation_list = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        rotated_prefix = ''.join([prefix[-i] for i in range(1, len(prefix))]) + prefix[0]
        for position, symbol in enumerate(rotated_prefix):
            tail_position = len(prefix) - 1 - position
            if symbol != 'Z':
                next_index = incrementation_list.index(symbol) + 1
                next_symbol = incrementation_list[next_index]
                incremented_prefix_list = [letter for letter in incremented_prefix]
                incremented_prefix_list[tail_position] = next_symbol
                incremented_prefix = ''.join(incremented_prefix_list)
                break
            else:
                incremented_prefix_list = [letter for letter in incremented_prefix]
                incremented_prefix_list[tail_position] = '0'
                incremented_prefix = ''.join(incremented_prefix_list)
        list_id = incremented_prefix + '-' + str(random.randint(1000000000, 9999999999))