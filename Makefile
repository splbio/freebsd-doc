# $FreeBSD$
#
# The user can override the default list of languages to build and install
# with the DOC_LANG variable.
#
.if defined(ENGLISH_ONLY) && !empty(ENGLISH_ONLY)
DOC_LANG=	en_US.ISO8859-1
.endif

.if defined(DOC_LANG) && !empty(DOC_LANG)
DOCSUBDIR = 	${DOC_LANG}
.else
DOCSUBDIR =	en_US.ISO8859-1
DOCSUBDIR+=	bn_BD.UTF-8
DOCSUBDIR+=	da_DK.ISO8859-1
DOCSUBDIR+=	de_DE.ISO8859-1
DOCSUBDIR+=	el_GR.ISO8859-7
DOCSUBDIR+=	es_ES.ISO8859-1
DOCSUBDIR+=	fr_FR.ISO8859-1
DOCSUBDIR+=	hu_HU.ISO8859-2
DOCSUBDIR+=	it_IT.ISO8859-15
DOCSUBDIR+=	ja_JP.eucJP
DOCSUBDIR+=	mn_MN.UTF-8
DOCSUBDIR+=	nl_NL.ISO8859-1
DOCSUBDIR+=	pl_PL.ISO8859-2
DOCSUBDIR+=	pt_BR.ISO8859-1
DOCSUBDIR+=	ru_RU.KOI8-R
DOCSUBDIR+=	sr_YU.ISO8859-2
DOCSUBDIR+=	tr_TR.ISO8859-9
DOCSUBDIR+=	zh_CN.UTF-8
DOCSUBDIR+=	zh_TW.UTF-8
.endif

SUBDIR+=	share ${DOCSUBDIR:C@([^ ]+)@website/templates/\1@g}

show:
	echo ${SUBDIR}

DOC_PREFIX?=   ${.CURDIR}

.export DOC_PREFIX

.if exists(/usr/bin/svnlite)
SVN?=		/usr/bin/svnlite
.else
SVN?=		/usr/local/bin/svn
.endif

update:
.if !exists(${SVN})
	@${ECHODIR} "--------------------------------------------------------------"
	@${ECHODIR} ">>> ${SVN} is required to update ${.CURDIR}"
	@${ECHODIR} "--------------------------------------------------------------"
	@${EXIT}
.else
	@${ECHODIR} "--------------------------------------------------------------"
	@${ECHODIR} ">>> Updating ${.CURDIR} from svn repository"
	@${ECHODIR} "--------------------------------------------------------------"
	cd ${.CURDIR}; ${SVN} update
.endif

.include "${DOC_PREFIX}/share/mk/doc.project.mk"
