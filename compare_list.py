import os
import sys
import time

def looking_for_diff(list_left, list_right, sort_method, compare_method):
    set_look_step = 30

    ret_list_del_1 = list()
    ret_list_del_2 = list()
    sort_method(list_left)
    sort_method(list_right)

    cmp_left_cur = 0
    cmp_left_point = 0
    cmp_right_cur = 0
    cmp_right_point = 0
    tic = 0

    while cmp_left_cur < len(list_left) or cmp_right_cur < len(list_right):
        if tic == 0:
            step_cnt = 0
            while True:
                if cmp_left_cur >= len(list_left):
                    tic = 1
                    break
                if cmp_left_point >= len(list_right):
                    ret_list_del_1.append(list_left[cmp_left_cur])
                    cmp_left_cur += 1
                    cmp_left_point = cmp_right_cur
                    tic = 1
                    break
                if step_cnt >= set_look_step:
                    tic = 1
                    break
                if compare_method(list_left[cmp_left_cur], list_right[cmp_left_point]):
                    # got one left and right is same
                    for item in list_right[cmp_right_cur:cmp_left_point]:
                        # now, we know some item in right-list which is missing in left-list
                        ret_list_del_2.append(item)
                    last_value = list_left[cmp_left_cur]
                    while cmp_left_point + 1 < len(list_right):
                        # in case same item in one list, we need to skip them
                        if compare_method(list_right[cmp_left_point + 1], last_value):
                            cmp_left_point += 1
                        else:
                            break
                    while cmp_left_cur + 1 < len(list_left):
                        # in case same items in one list, we need to skip them
                        if compare_method(list_left[cmp_left_cur + 1], last_value):
                            cmp_left_cur += 1
                        else:
                            break

                    cmp_left_cur += 1
                    cmp_left_point += 1
                    cmp_right_cur = cmp_left_point
                    cmp_right_point = cmp_left_cur

                    if cmp_left_cur >= len(list_left):
                        # now left-list reach its end, items remain in right-list is diffinetly missing in left-list
                        for item in list_right[cmp_right_cur:len(list_right)]:
                            ret_list_del_2.append(item)
                        # no need for right-list to find same in left-list, because left-list reach its end....
                        cmp_right_cur = len(list_right)
                        break

                else:
                    cmp_left_point += 1
                step_cnt += 1
        # mirror
        else:
            step_cnt = 0
            while True:
                if cmp_right_cur >= len(list_right):
                    tic = 0
                    break
                if cmp_right_point >= len(list_left):
                    ret_list_del_2.append(list_right[cmp_right_cur])
                    cmp_right_cur += 1
                    cmp_right_point = cmp_left_cur
                    tic = 0
                    break
                if step_cnt >= set_look_step:
                    tic = 0
                    break
                if compare_method(list_right[cmp_right_cur], list_left[cmp_right_point]):
                    for item in list_left[cmp_left_cur:cmp_right_point]:
                        ret_list_del_1.append(item)
                    last_value = list_right[cmp_right_cur]
                    while cmp_right_point+1 < len(list_left):
                        if compare_method(list_left[cmp_right_point + 1], last_value):
                            cmp_right_point += 1
                        else:
                            break
                    while cmp_right_cur + 1 < len(list_right):
                        if compare_method(list_right[cmp_right_cur + 1], last_value):
                            cmp_right_cur += 1
                        else:
                            break
                    cmp_right_cur += 1
                    cmp_right_point += 1
                    cmp_left_cur = cmp_right_point
                    cmp_left_point = cmp_right_cur

                    if cmp_right_cur >= len(list_right):
                        for item in list_left[cmp_left_cur:len(list_left)]:
                            ret_list_del_1.append(item)
                        cmp_left_cur = len(list_left)
                        break
                else:
                    cmp_right_point += 1
                step_cnt += 1
    return ret_list_del_1, ret_list_del_2
    pass

# define your own compare method
def compare_item(item_1, item_2):
    if item_1 == item_2:
        return True
    return False
    pass

# define you own sort method
def sort_list(item_list):
    item_list.sort()
    return
    pass


def diff_test_example():
    list_1 = [27,3,1,4,5,7,8,57,1,1,1,1]
    list_2 = [27,28,2,4,57,89,4578,57,1,1,1,1,1]
    (ret_del_1, ret_del_2) = looking_for_diff(list_1, list_2, sort_list, compare_item)
    print list_1
    print list_2
    print 'left_del'
    print ret_del_1
    print 'right del'
    print ret_del_2
    pass


