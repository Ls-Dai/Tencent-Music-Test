import pandas as pd
import numpy
import argparse


class SongDataset:
    def __init__(self, ROOT):
        self.df = pd.read_csv(ROOT)
        self.group = self.df.groupby("groupid")

    def fPlayRateByID(self, id):
        fplay_cnt_by_given_id = self.df[self.df.songid == id]["fplaycnt"]
        play_cnt_by_given_id = self.df[self.df.songid == id]["playcnt"]
        return fplay_cnt_by_given_id / play_cnt_by_given_id

    def fPlayRateByGroup_Find(self):
        # print(self.group.agg('sum'))
        # print(self.group.agg({'fplaycnt': 'sum', 'playcnt': 'sum'}))
        df_fplaycnt = self.group.agg({'fplaycnt': 'sum'})
        df_playcnt = self.group.agg({'playcnt': 'sum'})
        # print(df_playcnt)
        index_max = df_fplaycnt.idxmax()[0]
        # print(df_fplaycnt.loc[10, :][0])
        fplay_rate_by_index_max = df_fplaycnt.loc[10, :][0] / df_playcnt.loc[10, :][0]
        return df_fplaycnt.idxmax()[0], fplay_rate_by_index_max

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", type=int, default=-1, help="Song's ID")
    parser.add_argument("--hotest_group_data", action='store_true', help="...")
    parser.add_argument("--ROOT", type=str, default="data.csv")

    args = parser.parse_args()

    songDataset = SongDataset(args.ROOT)

    if (args.id != -1):
        fplayrate_by_id = songDataset.fPlayRateByID(args.id)
        print(
            "计算songid为{}的完播率: {:.3%}".format(args.id, float(fplayrate_by_id))
            )

    if (args.hotest_group_data == True):
        id, fplay_rate_by_index_max = songDataset.fPlayRateByGroup_Find() 
        print(
            "当多个songid隶属于同一个group时，其播放量和完播量合并计算，最后仅输出播放量最高的groupid和完播率: ID: {}, 完播率: {:.3%}".format(
            id, fplay_rate_by_index_max)
        )
