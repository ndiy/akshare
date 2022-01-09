# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2022/1/9 16:40
Desc: 东方财富网-数据中心-股东分析
https://data.eastmoney.com/gdfx/
"""
import pandas as pd
import requests
from tqdm import tqdm


def stock_gdfx_free_top_10_em(
    symbol: str = "sh688686", date: str = "20210630"
) -> pd.DataFrame:
    """
    东方财富网-个股-十大流通股东
    https://emweb.securities.eastmoney.com/PC_HSF10/ShareholderResearch/Index?type=web&code=SH688686#sdltgd-0
    :param symbol: 带市场标识的股票代码
    :type symbol: str
    :param date: 报告期
    :type date: str
    :return: 十大股东
    :rtype: pandas.DataFrame
    """
    url = (
        "https://emweb.securities.eastmoney.com/PC_HSF10/ShareholderResearch/PageSDLTGD"
    )
    params = {
        "code": f"{symbol.upper()}",
        "date": f"{'-'.join([date[:4], date[4:6], date[6:]])}",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["sdltgd"])
    temp_df.reset_index(inplace=True)
    temp_df["index"] = temp_df.index + 1
    temp_df.columns = [
        "名次",
        "-",
        "-",
        "-",
        "-",
        "股东名称",
        "股东性质",
        "股份类型",
        "持股数",
        "占总流通股本持股比例",
        "增减",
        "变动比率",
    ]
    temp_df = temp_df[
        [
            "名次",
            "股东名称",
            "股东性质",
            "股份类型",
            "持股数",
            "占总流通股本持股比例",
            "增减",
            "变动比率",
        ]
    ]
    temp_df["持股数"] = pd.to_numeric(temp_df["持股数"])
    temp_df["占总流通股本持股比例"] = pd.to_numeric(temp_df["占总流通股本持股比例"])
    temp_df["变动比率"] = pd.to_numeric(temp_df["变动比率"])
    return temp_df


def stock_gdfx_top_10_em(
    symbol: str = "sh688686", date: str = "20210630"
) -> pd.DataFrame:
    """
    东方财富网-个股-十大股东
    https://emweb.securities.eastmoney.com/PC_HSF10/ShareholderResearch/Index?type=web&code=SH688686#sdgd-0
    :param symbol: 带市场标识的股票代码
    :type symbol: str
    :param date: 报告期
    :type date: str
    :return: 十大股东
    :rtype: pandas.DataFrame
    """
    url = "https://emweb.securities.eastmoney.com/PC_HSF10/ShareholderResearch/PageSDGD"
    params = {
        "code": f"{symbol.upper()}",
        "date": f"{'-'.join([date[:4], date[4:6], date[6:]])}",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["sdgd"])
    temp_df.reset_index(inplace=True)
    temp_df["index"] = temp_df.index + 1
    temp_df.columns = [
        "名次",
        "-",
        "-",
        "-",
        "-",
        "股东名称",
        "股份类型",
        "持股数",
        "占总股本持股比例",
        "增减",
        "变动比率",
    ]
    temp_df = temp_df[
        [
            "名次",
            "股东名称",
            "股份类型",
            "持股数",
            "占总股本持股比例",
            "增减",
            "变动比率",
        ]
    ]
    temp_df["持股数"] = pd.to_numeric(temp_df["持股数"])
    temp_df["占总股本持股比例"] = pd.to_numeric(temp_df["占总股本持股比例"])
    temp_df["变动比率"] = pd.to_numeric(temp_df["变动比率"])
    return temp_df


def stock_gdfx_free_holding_analyse_em(date: str = "20210930") -> pd.DataFrame:
    """
    东方财富网-数据中心-股东分析-股东持股分析-十大流通股东
    https://data.eastmoney.com/gdfx/HoldingAnalyse.html
    :param date: 报告期
    :type date: str
    :return: 十大流通股东
    :rtype: pandas.DataFrame
    """
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "sortColumns": "UPDATE_DATE,SECURITY_CODE,HOLDER_RANK",
        "sortTypes": "-1,1,1",
        "pageSize": "500",
        "pageNumber": "1",
        "reportName": "RPT_CUSTOM_F10_EH_FREEHOLDERS_JOIN_FREEHOLDER_SHAREANALYSIS",
        "columns": "ALL;D10_ADJCHRATE,D30_ADJCHRATE,D60_ADJCHRATE",
        "source": "WEB",
        "client": "WEB",
        "filter": f"(END_DATE='{'-'.join([date[:4], date[4:6], date[6:]])}')",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    total_page = data_json["result"]["pages"]
    big_df = pd.DataFrame()
    for page in tqdm(range(1, total_page + 1)):
        params.update({"pageNumber": page})
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["result"]["data"])
        big_df = big_df.append(temp_df, ignore_index=True)
    big_df.reset_index(inplace=True)
    big_df["index"] = big_df.index + 1
    big_df.columns = [
        "序号",
        "-",
        "股票代码",
        "-",
        "-",
        "股东名称",
        "期末持股-数量",
        "-",
        "-",
        "-",
        "-",
        "-",
        "股票简称",
        "-",
        "-",
        "-",
        "期末持股-流通市值",
        "-",
        "-",
        "期末持股-数量变化比例",
        "股东类型",
        "-",
        "公告日",
        "报告期",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "期末持股-持股变动",
        "-",
        "-",
        "-",
        "-",
        "期末持股-数量变化",
        "公告日后涨跌幅-10个交易日",
        "公告日后涨跌幅-30个交易日",
        "公告日后涨跌幅-60个交易日",
    ]
    big_df = big_df[
        [
            "序号",
            "股东名称",
            "股东类型",
            "股票代码",
            "股票简称",
            "报告期",
            "期末持股-数量",
            "期末持股-数量变化",
            "期末持股-数量变化比例",
            "期末持股-持股变动",
            "期末持股-流通市值",
            "公告日",
            "公告日后涨跌幅-10个交易日",
            "公告日后涨跌幅-30个交易日",
            "公告日后涨跌幅-60个交易日",
        ]
    ]
    big_df["公告日"] = pd.to_datetime(big_df["公告日"]).dt.date
    big_df["期末持股-数量"] = pd.to_numeric(big_df["期末持股-数量"])
    big_df["期末持股-数量变化"] = pd.to_numeric(big_df["期末持股-数量变化"])
    big_df["期末持股-数量变化比例"] = pd.to_numeric(big_df["期末持股-数量变化比例"])
    big_df["期末持股-流通市值"] = pd.to_numeric(big_df["期末持股-流通市值"])
    big_df["公告日后涨跌幅-10个交易日"] = pd.to_numeric(big_df["公告日后涨跌幅-10个交易日"])
    big_df["公告日后涨跌幅-30个交易日"] = pd.to_numeric(big_df["公告日后涨跌幅-30个交易日"])
    big_df["公告日后涨跌幅-60个交易日"] = pd.to_numeric(big_df["公告日后涨跌幅-60个交易日"])
    return big_df


def stock_gdfx_holding_analyse_em(date: str = "20210930") -> pd.DataFrame:
    """
    东方财富网-数据中心-股东分析-股东持股分析-十大股东
    https://data.eastmoney.com/gdfx/HoldingAnalyse.html
    :param date: 报告期
    :type date: str
    :return: 十大股东
    :rtype: pandas.DataFrame
    """
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "sortColumns": "NOTICE_DATE,SECURITY_CODE,RANK",
        "sortTypes": "-1,1,1",
        "pageSize": "500",
        "pageNumber": "1",
        "reportName": "RPT_CUSTOM_DMSK_HOLDERS_JOIN_HOLDER_SHAREANALYSIS",
        "columns": "ALL;D10_ADJCHRATE,D30_ADJCHRATE,D60_ADJCHRATE",
        "source": "WEB",
        "client": "WEB",
        "filter": f"(END_DATE='{'-'.join([date[:4], date[4:6], date[6:]])}')",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    total_page = data_json["result"]["pages"]
    big_df = pd.DataFrame()
    for page in tqdm(range(1, total_page + 1)):
        params.update({"pageNumber": page})
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["result"]["data"])
        big_df = big_df.append(temp_df, ignore_index=True)
    big_df.reset_index(inplace=True)
    big_df["index"] = big_df.index + 1
    big_df.columns = [
        "序号",
        "-",
        "股票代码",
        "-",
        "-",
        "报告期",
        "-",
        "-",
        "股东名称",
        "期末持股-数量",
        "-",
        "期末持股-数量变化",
        "期末持股-数量变化比例",
        "-",
        "-",
        "股东类型",
        "-",
        "-",
        "公告日",
        "-",
        "-",
        "-",
        "股票简称",
        "-",
        "-",
        "期末持股-流通市值",
        "期末持股-持股变动",
        "-",
        "-",
        "-",
        "-",
        "公告日后涨跌幅-10个交易日",
        "公告日后涨跌幅-30个交易日",
        "公告日后涨跌幅-60个交易日",
    ]
    big_df = big_df[
        [
            "序号",
            "股东名称",
            "股东类型",
            "股票代码",
            "股票简称",
            "报告期",
            "期末持股-数量",
            "期末持股-数量变化",
            "期末持股-数量变化比例",
            "期末持股-持股变动",
            "期末持股-流通市值",
            "公告日",
            "公告日后涨跌幅-10个交易日",
            "公告日后涨跌幅-30个交易日",
            "公告日后涨跌幅-60个交易日",
        ]
    ]
    big_df["公告日"] = pd.to_datetime(big_df["公告日"]).dt.date
    big_df["期末持股-数量"] = pd.to_numeric(big_df["期末持股-数量"])
    big_df["期末持股-数量变化"] = pd.to_numeric(big_df["期末持股-数量变化"])
    big_df["期末持股-数量变化比例"] = pd.to_numeric(big_df["期末持股-数量变化比例"])
    big_df["期末持股-流通市值"] = pd.to_numeric(big_df["期末持股-流通市值"])
    big_df["公告日后涨跌幅-10个交易日"] = pd.to_numeric(big_df["公告日后涨跌幅-10个交易日"])
    big_df["公告日后涨跌幅-30个交易日"] = pd.to_numeric(big_df["公告日后涨跌幅-30个交易日"])
    big_df["公告日后涨跌幅-60个交易日"] = pd.to_numeric(big_df["公告日后涨跌幅-60个交易日"])
    return big_df


if __name__ == "__main__":
    stock_gdfx_free_top_10_em_df = stock_gdfx_free_top_10_em(
        symbol="sh688686", date="20210630"
    )
    print(stock_gdfx_free_top_10_em_df)

    stock_gdfx_top_10_em_df = stock_gdfx_top_10_em(symbol="sh688686", date="20210630")
    print(stock_gdfx_top_10_em_df)

    stock_gdfx_free_holding_analyse_em_df = stock_gdfx_free_holding_analyse_em(
        date="20210930"
    )
    print(stock_gdfx_free_holding_analyse_em_df)

    stock_gdfx_holding_analyse_em_df = stock_gdfx_holding_analyse_em(date="20210930")
    print(stock_gdfx_holding_analyse_em_df)
