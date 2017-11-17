begin;
declare @gsdm varchar(25)
declare @count int;
declare @time varchar(19);
declare @date varchar(10);
declare @gysMc1 varchar(500);
declare @gysMc2 varchar(500);
declare @ywyMc1 varchar(500);
declare @ywyMc2 varchar(500);
declare @khMc1 varchar(500);
declare @khMc2 varchar(500);
declare @spMc1 varchar(500);
declare @sp1_chcd varchar(500);
declare @spMc2 varchar(500);
declare @sp2_chcd varchar(500);
declare @ckMc1 varchar(500) ;
declare @ckMc2 varchar(500) ;
declare @zhMc1 varchar(500) ;
declare @zhMc2 varchar(500) ;
declare @sp_hsfs varchar(10) ;
set @gsdm = '$gsdm$';
set @gysMc1='$gysMc1$';
set @gysMc2='$gysMc2$';
set @ywyMc1='$ywyMc1$';
set @ywyMc2='$ywyMc2$';
set @khMc1='$khMc1$';
set @khMc2='$khMc2$';
set @zhMc1='$zhMc1$';
set @zhMc2='$zhMc2$';
set @ckMc1 = '$ckMc1$' ;
set @ckMc2 = '$ckMc2$' ;
set @sp_hsfs = '$sp_hsfs$';
set @spMc1 = '$spMc1$';
set @sp1_chcd='$sp1_chcd$';
set @spMc2 = '$spMc2$';
set @sp2_chcd='$sp2_chcd$';

set @time = convert(varchar(19),getdate(),120) ;
set @date = convert(varchar(10),getdate(),120) ;
--创建供应商
select @count = count(1) from dm_gys where gsdm = @gsdm and yxbz='y' and name = @gysMc1;
if @count = 0
	insert INTO dm_gys ([name],[yxbz],[xyed],[lrrq], [xgrq],[gsdm]) VALUES ( @gysMc1,'Y','0', @time, @time, @gsdm) ;
select @count = count(1) from dm_gys where gsdm = @gsdm and yxbz='y' and name = @gysMc2;
if @count = 0
	insert INTO dm_gys ([name],[yxbz],[xyed],[lrrq], [xgrq],[gsdm]) VALUES ( @gysMc2,'Y','0', @time, @time, @gsdm) ;
--创建业务员
select @count = count(1) from xt_user where gsdm = @gsdm and yxbz='y' and name = @ywyMc2;
if @count = 0
	INSERT INTO xt_user ([name],[yxbz], [yhlx], [loginname], [password], [jbgz], [ckjg], [cxts], [xgdj], [lrrq], [xgrq], [gsdm], [khdm], [dyjf], [rjbsk], [ycckj], [appstoreuserid], [ychm], [ckxsb], [sfcgywy], [moashzt], [xgfzkh]) VALUES ( @ywyMc2, 'Y','业务员', '', '', '0', 'N', '2', 'N', @time, @time, @gsdm, '0', '0', 'N', 'N', '0', 'N', 'N', 'N', 'N', 'N');
select @count = count(1) from xt_user where gsdm = @gsdm and yxbz='y' and name = @ywyMc1;
if @count = 0
	INSERT INTO xt_user ([name],[yxbz], [yhlx], [loginname], [password], [jbgz], [ckjg], [cxts], [xgdj], [lrrq], [xgrq], [gsdm], [khdm], [dyjf], [rjbsk], [ycckj], [appstoreuserid], [ychm], [ckxsb], [sfcgywy], [moashzt], [xgfzkh]) VALUES ( @ywyMc1, 'Y','业务员', '', '', '0', 'N', '2', 'N', @time, @time, @gsdm, '0', '0', 'N', 'N', '0', 'N', 'N', 'N', 'N', 'N');
--创建银行账号
select @count = count(1) from cw_zhxx where gsdm = @gsdm and yxbz='y' and name = @zhMc1;
if @count = 0
	INSERT INTO cw_zhxx ([zhlx], [name], [yxbz], [gsdm]) VALUES ('银行账', @zhMc1, 'Y', @gsdm);
select @count = count(1) from cw_zhxx where gsdm = @gsdm and yxbz='y' and name = @zhMc2;
if @count = 0
	INSERT INTO cw_zhxx ([zhlx], [name], [yxbz], [gsdm]) VALUES ('现金账', @zhMc2, 'Y', @gsdm);
--创建客户
select @count = count(1) from dm_khxx where gsdm = @gsdm and yxbz='y' and name = @khMc1;
if @count = 0
	insert INTO dm_khxx ([name], [yxbz], [lrrq], [xgrq], [sled], [gsdm]) VALUES (@khMc1, 'Y', @time, @time, '0', @gsdm);
select @count = count(1) from dm_khxx where gsdm = @gsdm and yxbz='y' and name = @khMc2;
if @count = 0
	insert INTO dm_khxx ([name], [yxbz], [lrrq], [xgrq], [sled], [gsdm]) VALUES (@khMc2, 'Y', @time, @time, '0', @gsdm);
--创建仓库
select @count = count(1) from dm_ckxx where gsdm = @gsdm and yxbz='y' and name = @ckMc1;
if @count = 0
	INSERT INTO dm_ckxx ([gsdm], [name], [yxbz], [xyed], [zq], [lrrq], [xgrq], [sfks], [sfkjh], [mrck]) VALUES (@gsdm, @ckMc1, 'Y', '0', '0', @time, @time, 'Y', 'N', 'N');
select @count = count(1) from dm_ckxx where gsdm = @gsdm and yxbz='y' and name = @ckMc2;
if @count = 0
	INSERT INTO dm_ckxx ([gsdm], [name], [yxbz], [xyed], [zq], [lrrq], [xgrq], [sfks], [sfkjh], [mrck]) VALUES (@gsdm, @ckMc2, 'Y', '0', '0', @time, @time, 'Y', 'N', 'N') ;
--创建商品
select @count = count(1) from dm_spxx where gsdm = @gsdm and yxbz='y' and fullname = @spMc1;
if @count = 0
	INSERT INTO dm_spxx ([gsdm], [yxbz], [fullname], [name], [km], [hsfs], [chcd], [pp], [color], [kcsx], [kcxx],[yxkl], [lrrq], [xgrq]) VALUES (@gsdm, 'Y', @spMc1, '诺基亚N97', '手机', @sp_hsfs, @sp1_chcd, '诺基亚', '灰', '0', '0', '0', @time, @time)
else
	update dm_spxx set chcd=@sp1_chcd,hsfs=@sp_hsfs where gsdm = @gsdm and yxbz='y' and fullname = @spMc1;
select @count = count(1) from dm_spxx where gsdm = @gsdm and yxbz='y' and fullname = @spMc2;
if @count = 0
	INSERT INTO dm_spxx ([gsdm], [yxbz], [fullname], [name], [km], [hsfs], [chcd], [pp], [color], [kcsx], [kcxx],[yxkl], [lrrq], [xgrq]) VALUES (@gsdm, 'Y', @spMc2, '诺基亚N97', '手机', @sp_hsfs, @sp2_chcd, '诺基亚', '黑', '0', '0', '0', @time, @time)
else
	update dm_spxx set chcd=@sp2_chcd,hsfs=@sp_hsfs where gsdm = @gsdm and yxbz='y' and fullname = @spMc2;
end;

