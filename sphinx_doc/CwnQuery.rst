API Quick Start
--------------


.. container:: cell markdown

   .. rubric:: Cwn Graph Query
      :name: cwn-graph-query

.. container:: cell code

   .. code:: python

      %load_ext autoreload
      %autoreload 2

.. container:: cell code

   .. code:: python

      import pickle
      from CwnGraph import CwnBase, CwnAnnotator
      from CwnGraph import CwnRelationType

.. container:: cell markdown

   CwnGraph can be installed as a package. When run first time, prepare
   cwn_graph.pyobj and install with install_cwn(). After installation,
   CwnGraph use CWN data in its own home directory, regardless of
   working directory.

.. container:: cell code

   .. code:: python

      cwn = CwnBase.install_cwn("data/cwn_graph.pyobj")

   .. container:: output stream stdout

      ::

         CWN data installed

.. container:: cell code

   .. code:: python

      cwn = CwnBase()

.. container:: cell code

   .. code:: python

      # this line may take a few seconds
      cwn.get_hash()

   .. container:: output execute_result

      ::

         '5d536f'

.. container:: cell markdown

   .. rubric:: Basic Query
      :name: basic-query

.. container:: cell code

   .. code:: python

      lemmas = cwn.find_lemma("電腦")
      print(lemmas)

   .. container:: output stream stdout

      ::

         [<CwnLemma: 電腦_1>, <CwnLemma: 電腦化_1>, <CwnLemma: 微電腦_1>]

.. container:: cell code

   .. code:: python

      lemma0 = lemmas[0]
      senses = lemma0.senses
      print(senses)

   .. container:: output stream stdout

      ::

         [<CwnSense[06613601](電腦): 一種資料處理裝置，能自動接受並儲存、處理輸入的資料，然後經由一組預先存放在機器內的指令逐步引導下產生輸出結果。>, <CwnSense[06613602](電腦): 研究或操作電腦的知識。>, <CwnSense[06613603](電腦): 比喻計算或記憶能力很強的人。>]

.. container:: cell code

   .. code:: python

      for sense_x in senses:
          print(sense_x)
          print(sense_x.relations)
          print("--")

   .. container:: output stream stdout

      ::

         <CwnSense[06613601](電腦): 一種資料處理裝置，能自動接受並儲存、處理輸入的資料，然後經由一組預先存放在機器內的指令逐步引導下產生輸出結果。>
         [('has_facet', <CwnFacet[0661360101](電腦): 普通名詞。電腦的功能，通常包括程式、軟體等。>), ('has_facet', <CwnFacet[0661360102](電腦): 普通名詞。電腦的實體，特別指外表，通常包括螢幕、鍵盤、主機等。>), ('is_synset', <CwnSense[syn_004128](----): >), ('hypernym', <CwnSense[06582901](工具): 工作時必須使用的具有特定功能的器具。>), ('hyponym(rev)', <CwnSense[06582901](工具): 工作時必須使用的具有特定功能的器具。>)]
         --
         <CwnSense[06613602](電腦): 研究或操作電腦的知識。>
         [('is_synset', <CwnSense[syn_016365](----): >)]
         --
         <CwnSense[06613603](電腦): 比喻計算或記憶能力很強的人。>
         [('is_synset', <CwnSense[syn_014518](----): >)]
         --

.. container:: cell code

   .. code:: python

      senses[1].data()

   .. container:: output execute_result

      ::

         {'node_type': 'sense',
          'pos': 'Na',
          'examples': ['小朋友都覺得放假好煩，比上學更累，他們要學<電腦>，上補習班。\r\n',
           '這樣規定豈不是加重學生的負擔？還不如學<電腦>或英文更有實效。\r\n',
           '陶公我在高一時就認為他<電腦>超強的，但是現在我認為muscle你也不差。\r\n'],
          'domain': '',
          'annot': {},
          'def': '研究或操作電腦的知識。'}

.. container:: cell code

   .. code:: python

      cwn.find_senses(lemma="^車$")

   .. container:: output execute_result

      ::

         [<CwnSense[06665201](車): 在陸地上以輪子行駛的運輸工具。>,
          <CwnSense[06665202](車): 以車子為形象製成的人造物。>,
          <CwnSense[06665203](車): 開放式用於乘載或放置物品的有輪子的工具。>,
          <CwnSense[06665204](車): 相互連結用在軌道上行駛的運輸工具中的一節。>,
          <CwnSense[06665205](車): 計算一車承載物的量的單位。>,
          <CwnSense[06665206](車): 利用機械切削特定物品。>,
          <CwnSense[06665207](車): 大型的紡織機械。>,
          <CwnSense[06665208](車): 利用機器來縫製衣物。>,
          <CwnSense[07021501](車): 姓。>,
          <CwnSense[07021601](車): 象棋遊戲中所使用的棋子之一，走直線。>]

.. container:: cell code

   .. code:: python

      cwn.find_senses(definition="輪子")

   .. container:: output execute_result

      ::

         [<CwnSense[03027001](輛): 計算有輪子的機械裝置的單位。>,
          <CwnSense[04082906](台): 計算有輪子的機械裝置的單位。>,
          <CwnSense[04153906](臺): 計算有輪子的機械裝置的單位。>,
          <CwnSense[05075709](部): 計算有輪子的機械裝置的單位。>,
          <CwnSense[05131903](輪): 計算輪子的單位。>,
          <CwnSense[05131904](輪): 形狀像輪子的物體。>,
          <CwnSense[06521401](車子): 在陸地上以輪子行駛的運輸工具。>,
          <CwnSense[06552201](汽車): 在陸地上行駛的有四個以上的輪子的運輸工具。>,
          <CwnSense[06665201](車): 在陸地上以輪子行駛的運輸工具。>,
          <CwnSense[06665203](車): 開放式用於乘載或放置物品的有輪子的工具。>,
          <CwnSense[08008101](胎): 輪子外面包覆的環形橡膠製品。為英語tire的音譯。>,
          <CwnSense[09004101](汽): 在陸地上行駛的有四個以上的輪子的運輸工具。>]

.. container:: cell code

   .. code:: python

      cwn.find_senses(examples="學步車")

   .. container:: output execute_result

      ::

         [<CwnSense[05041401](連): 兩物體在空間上相連。>,
          <CwnSense[06665203](車): 開放式用於乘載或放置物品的有輪子的工具。>]

.. container:: cell code

   .. code:: python

      spend_senses = cwn.find_senses(lemma="花費")
      spend_senses[0].facets

   .. container:: output execute_result

      ::

         [<CwnFacet[0506490101](花費): 消耗後述時間或能量。>,
          <CwnFacet[0506490102](花費): 付出金錢。>,
          <CwnFacet[0506490103](花費): 付出金錢。>]

.. container:: cell code

   .. code:: python

      spend_senses[0].examples

   .. container:: output execute_result

      ::

         ''

.. container:: cell code

   .. code:: python

      spend_senses[0].all_examples()

   .. container:: output execute_result

      ::

         ['總統對中油努力探勘油源所<花費>的心力，表示肯定。',
          '因為資訊實在太多，即使走馬看花，也要<花費>不少時間。',
          '薄薄的一張證明，又不需要<花費>很大人力，卻要索價三百元。',
          '第一階段選擇場址評估約需<花費>一千五百萬元。',
          'IBM相當重視研究開發，每年<花費>在此方面的經費不下數十億美元。',
          '整體經營與制度化，導致包括交通、住宿及其他<花費>的資金，大多未能流入當地社會。',
          '職業訓練是投資，而不是<花費>。',
          '只要有興趣，就不會在乎金錢上的<花費>。',
          '計有卅八宗個案，<花費>金額為四十六萬五千五百廿五元。']
