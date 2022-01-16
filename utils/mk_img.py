import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.ticker import MaxNLocator


def create_svg(title, datas, save_path):

    fig, ax = plt.subplots(figsize=(12, 5))

    # 设置透明
    fig.patch.set_alpha(.0)
    ax.patch.set_alpha(.0)

    # 坐标
    ax.tick_params(color='darkgrey', labelcolor='darkgrey')

    # 坐标轴
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_color("darkgrey")
    ax.spines['left'].set_color("darkgrey")
    ax.spines['right'].set_color('none')

    # 绘线
    for k, data in datas.items():
        date_list = data["date_list"]
        num_list = data["num_list"]
        name = k
        ax.plot(date_list, num_list, label=name)

    # 图例
    ax.legend(
        frameon=False,
        # loc=2,
        # bbox_to_anchor=(1.05, 0.0, 3.0, 0.0),
        borderaxespad = 0.,
        labelcolor='darkgrey'
    )

    # 标题
    ax.set_title(f"{title}", color='darkgrey')

    # 网格
    ax.grid(True, linestyle='-.')

    plt.savefig(save_path)

if __name__ == "__main__":
    data_list = [
    {
      "id": 2897,
      "server": "长安城",
      "wanbaolou": "708.00",
      "tieba": "740.00",
      "dd373": "720.00",
      "uu898": "732.98",
      "5173": "720.00",
      "7881": "700.00",
      "time": 1637331340
    },
    {
      "id": 2792,
      "server": "长安城",
      "wanbaolou": "708.00",
      "tieba": "740.00",
      "dd373": "625.00",
      "uu898": "726.00",
      "5173": "720.00",
      "7881": "700.00",
      "time": 1637250378
    },
    {
      "id": 2672,
      "server": "长安城",
      "wanbaolou": "704.00",
      "tieba": "740.00",
      "dd373": "626.00",
      "uu898": "726.00",
      "5173": "652.96",
      "7881": "700.00",
      "time": 1637158130
    },
    {
      "id": 2567,
      "server": "长安城",
      "wanbaolou": "704.00",
      "tieba": "740.00",
      "dd373": "734.69",
      "uu898": "726.00",
      "5173": "652.96",
      "7881": "700.00",
      "time": 1637077219
    },
    {
      "id": 2447,
      "server": "长安城",
      "wanbaolou": "705.00",
      "tieba": "740.00",
      "dd373": "726.00",
      "uu898": "726.00",
      "5173": "700.00",
      "7881": "700.00",
      "time": 1636984631
    },
    {
      "id": 2342,
      "server": "长安城",
      "wanbaolou": "705.00",
      "tieba": "730.00",
      "dd373": "721.00",
      "uu898": "711.66",
      "5173": "652.96",
      "7881": "700.00",
      "time": 1636903521
    },
    {
      "id": 2215,
      "server": "长安城",
      "wanbaolou": "705.00",
      "tieba": "740.00",
      "dd373": "730.00",
      "uu898": "712.12",
      "5173": "730.00",
      "7881": "700.00",
      "time": 1636811007
    },
    {
      "id": 2110,
      "server": "长安城",
      "wanbaolou": "706.00",
      "tieba": "740.00",
      "dd373": "757.89",
      "uu898": "725.00",
      "5173": "710.00",
      "7881": "700.00",
      "time": 1636730245
    },
    {
      "id": 1990,
      "server": "长安城",
      "wanbaolou": "703.00",
      "tieba": "740.00",
      "dd373": "723.00",
      "uu898": "728.01",
      "5173": "712.40",
      "7881": "700.00",
      "time": 1636637814
    },
    {
      "id": 1885,
      "server": "长安城",
      "wanbaolou": "703.00",
      "tieba": "740.00",
      "dd373": "730.31",
      "uu898": "728.01",
      "5173": "730.00",
      "7881": "700.00",
      "time": 1636557148
    }
  ]
    key_list = [
        "wanbaolou",
        "tieba",
        "dd373",
        "uu898",
        "5173",
        "7881"
    ]
    datas = {}
    for i in data_list[::-1]:
        for k, v in i.items():
            if k in key_list:
                if k not in datas:
                    datas[k] = {
                        "date_list": [],
                        "num_list": []
                    }
                datas[k]["date_list"].append(datetime.fromtimestamp(i["time"]).strftime('%Y-%m-%d'))
                datas[k]["num_list"].append(float(i[k]))
    save_path = "aaa.png"
    create_svg("111", datas, save_path)