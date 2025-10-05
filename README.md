# ymvdec
用于拆解yuris引擎ymv文件的python脚本。/Python script for unpacking ymv files from the Yuris engine.

usage:
ymvdec.py <ymvFilePath> <outputDir>

本来是wmv文件的只会改后缀，逐帧图片合成的ymv会被拆解成表示rgb和透明度(如果有)的多张jpg。
