regular_widget
================================================================
仅仅对于char类型的字段生效
================================================================
使用方式如下：
例子：只能输入5位的英文和数字
<field name="test1" widget="regex_mask" data-inputmask-regex="^[A-Za-z0-9]{5}$"/>

================================================================
其他：
<field widget="mask" data-inputmask="'alias': 'date'" name="name" />
<field widget="mask" data-inputmask="'mask': '99/99/9999'" name="name" />
<field widget="mask" data-inputmask="'mask': '99-aa-**-AA-&amp;&amp;-##'" name="name" />
<field widget="mask" data-inputmask="'mask': '9', 'repeat': 10, 'greedy' : false" name="name" />
<field widget="mask" data-inputmask-alias="date" name="name" />
<field widget="mask" data-inputmask-mask="99/99/9999" name="name" />
<field widget="mask" data-inputmask-mask="99-aa-**-AA-&amp;&amp;-##" name="name" />
<field widget="mask" data-inputmask-mask="9" data-inputmask-repeat="10" data-inputmask-greedy="false" name="name" />
<field widget="regex_mask" data-inputmask-regex="[a-zA-Z0-9._%-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,4}" name="name"/>
