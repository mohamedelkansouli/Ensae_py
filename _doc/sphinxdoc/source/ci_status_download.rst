
Pypi download
=============

.. index:: pypi, pypi download

Le nombre de téléchargements peut être
obtenu en exécutant la requête suivante sur
`Google BigQuery <https://bigquery.cloud.google.com/results/>`_.

.. runpython::

    query = """
    #standardSQL
    SELECT
      file.project as Project,
      COUNT(*) AS num_downloads,
      SUBSTR(_TABLE_SUFFIX, 1, 6) AS `month`
    FROM `the-psf.pypi.downloads*`
    WHERE
      __CONDITION__
      -- Only query the last 6 months of history
      AND _TABLE_SUFFIX
        BETWEEN FORMAT_DATE(
          '%Y%m01', DATE_SUB(CURRENT_DATE(), INTERVAL 12 MONTH))
        AND FORMAT_DATE('%Y%m%d', CURRENT_DATE())
    GROUP BY `month`, `Project`
    """

    from ensae_teaching_cs.automation import get_teaching_modules
    modules = get_teaching_modules()
    conds = ["file.project = '{0}'".format(m) for m in modules]
    cond = " OR ".join(conds)
    print(query.replace('__CONDITION__', cond))

.. plot::

    import pandas
    import matplotlib.pyplot as plt

    df = pandas.read_csv('pypi_downloads.csv')
    df = df.sort_values(["Project", "month"])
    df['month'] = df.month.astype(str)
    df = df[df.month >= "2017"]
    gr = df.groupby("Project", as_index=False).sum().sort_values("num_downloads").reset_index(drop=True)
    med = gr.iloc[gr.shape[0]//2, 1]
    nb = 4
    sets = []
    for i in range(nb):
        if i == nb-1:
            sets.append(set(gr.iloc[i*gr.shape[0]//nb:, 0]))
        else:
            sets.append(set(gr.iloc[i*gr.shape[0]//nb:(i+1)*gr.shape[0]//nb, 0]))

    piv = df.pivot("month", "Project", "num_downloads").fillna(0)

    fig, ax = plt.subplots(nb, 1, figsize=(12,16))
    colormaps = ['Accent', "tab10", "Paired", "tab20"]
    for i in range(nb):
        piv2 = piv[[_ for _ in sets[nb-i-1]]]
        piv2.plot.area(colormap=colormaps[i], ax=ax[i])
        ax[i].set_xticks(list(range(0, len(piv2.index), 2)))
        ax[i].set_xticklabels(list(piv2.index)[::2])
    plt.show()
