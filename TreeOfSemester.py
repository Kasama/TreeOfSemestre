def mainLoad( ano ):
    MainTreeFile = open( "main/" + ano , "r" )
    TreeOrder = []
    MainTree = {}
    lastVert = None
    for line in MainTreeFile.readlines():
        if( line.find(">") >= 0 ):
            if( lastVert is not None ):
                line = line.strip()
                lastVert["dependencias"].append( line[ 1: ] )
        elif( line.find("~") >= 0 ):
            pass
        else:
            if( lastVert is not None ):
                MainTree.update( { lastVert["sigla"] : lastVert} )
            s, n = line.split("-")
            TreeOrder.append( s )
            lastVert = { "nome": n, "sigla": s, "dependencias": [], "trancamentosDiretos": [], "trancamentosTotais": -1, "listaTrancamentos": {}, "participacao": -1 }

    MainTree.update( {lastVert["sigla"] : lastVert} )
    return MainTree, TreeOrder

def calculaTrancamentosTotaisR( node, tree ):
    if( tree[ node ]["trancamentosTotais"] < 0 ):
        for n in tree[ node ]["trancamentosDiretos"]:
            calculaTrancamentosTotaisR( n, tree )
            tree[ node ]["listaTrancamentos"].update( tree[ n ]["listaTrancamentos"] )
            tree[ node ]["listaTrancamentos"].update( { n: tree[ n ]["trancamentosTotais"] } )
        tree[ node ]["trancamentosTotais"] = len( tree[ node ]["listaTrancamentos"] )

def calculaTrancamentosTotais( tree ):
    for k in tree:
        calculaTrancamentosTotaisR( k, tree )

def calculaTrancamentosDiretos( tree ):
    for k in tree:
        for n in tree[ k ]["dependencias"]:
            try:
                tree[ n ]["trancamentosDiretos"].append( k )
            except Exception as e:
                print( "Erro nas dependencias de ", k )
                print( e )

def TopologiaDaTranca( tree ):
    estat = {}
    for v in tree:
        try:
            estat.update( { tree[ v ]["trancamentosTotais"]: estat[ tree[ v ]["trancamentosTotais"] ] + 1 } )
        except:
            estat.update( { tree[ v ]["trancamentosTotais"]: 1 } )

    print( "Nro de Trancamentos    -    Nro de Disciplinas   -   Porcentagem do Total")
    for k in estat:
        print( "     ", k, "     -     ", estat[ k ], "     -     ", "( ", ( 100 * ( estat[ k ] / len( tree ) ) ), "%)")

def printTree( tree, order ):
    print( "Sigla  -  Nome")
    for v in order:
        print( tree[ v ]["sigla"] + "  -  " + tree[ v ]["nome"] )

def filtraTrancamento( tree ):
    print( "Quantos trancamentos? (n ou mais)")
    n = int( input() )
    count = 0
    for v in tree:
        if( tree[ v ]["trancamentosTotais"] >= n ):
            print( "\n" + tree[ v ]["sigla"] + "  -  " + tree[ v ]["nome"].strip() + "  -  " + str( tree[ v ]["trancamentosTotais"] ) + "\n" )
            count = count + 1
            for each in tree[ v ]["listaTrancamentos"]:
                print(" > " + each + tree[ each ]["nome"].strip() )
    print("\nTotal: ", count)

def criaUserTree( tree, order, forest, ano ):
    print( "Nusp: ")
    nusp = input()
    dummyOrder = []
    dummyOrder.extend( order )
    UserTree = []
    print("Você já cursou: (s - Sim, n - Não, p - Quebrou o Pré)\n")
    for each in dummyOrder:
        print( each + " - " + tree[each]["nome"] + "? " )
        ans = input()
        if( ans == "s"):
            UserTree.append( each )
        elif( ans == "n" ):
            for k in tree[ each ]["listaTrancamentos"]:
                try:
                    dummyOrder.remove( k )
                except:
                    pass
        elif( ans == "p" ):
            pass
        else:
            print("Poxa cara, é um negócio sério\n")
            return criaUserTree( tree, order )
    try:
        savefile = open( "data/" + ano + "/" + nusp, "w" )
        dummystr = ""
        for k in UserTree:
            dummystr = dummystr + "/" + k

        savefile.write( dummystr[1:] )
        savefile.close()

    except:
        print( "Deu escrotamente ruim. Tente novamente =/" )

    print( "Arvore criada! Obrigado.")
    with open( "data/" + ano + "/index", "a" ) as TreeIndex:
        TreeIndex.write(nusp)
    forest.update( { nusp: UserTree } )
    return UserTree

def carregaUserTrees( ano ):
    with open( "data/" + ano + "/index", "r" ) as TreeIndex:
        UserForest = {}
        for line in TreeIndex.readlines():
            line = line.strip()
            try:
                dummyfile = open( "data/" + ano + "/" + line, "r" )
                dummylist = []
                dummystr = dummyfile.read()
                dummylist.extend( dummystr.split("/") )
                UserForest.update( { line: dummylist })
                dummyfile.close()
            except:
                pass
    return UserForest

def PorcentagemDeCompletude( tree, forest, order ):
    YearTree = {}
    for q in order:
        for w in forest:
            if( q in forest[ w ] ):
                try:
                    YearTree.update( { q: YearTree[q] + 1 } )
                except:
                    YearTree.update( { q: 1 } )
    for q in order:
        try:
            if( YearTree[q] > 0 ):
                print( tree[q]["sigla"] + " - " + tree[q]["nome"].strip() + ": ")
                print( YearTree[q], " / ", len(forest), " (", (100 * ( YearTree[q] / len(forest) ) ), ") ")
        except:
            pass

if __name__ == "__main__":
    print( "Ano de Ingresso: ")
    ano = input()
    MainTree, TreeOrder = mainLoad( ano )
    calculaTrancamentosDiretos( MainTree )
    calculaTrancamentosTotais( MainTree )
    UserForest = carregaUserTrees( ano )
    op = 1
    while( op ):
        print( "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        print( "Menu: \n1 - Cadastrar Arvore de Usuario\n2 - Imprimir Grade do Ano\n3 - Estatisticas\n0 - Sair")
        op = input()
        if( op == "1" ):
            print( "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
            criaUserTree( MainTree, TreeOrder, UserForest, ano )
        if( op == "2" ):
            print( "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
            printTree( MainTree, TreeOrder )
            dummy = input()
        if( op == "3" ):
            print( "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
            print( "Menu: \n1 - Topologia da Tranca\n2 - Porcentagem de Completude\n3 - Filtrar por Trancamentos")
            op = input()
            if( op == "1" ):
                print( "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
                TopologiaDaTranca( MainTree )
                dummy = input()
            if( op == "2" ):
                print( "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
                PorcentagemDeCompletude( MainTree, UserForest, TreeOrder )
                dummy = input()
            if( op == "3" ):
                print( "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
                filtraTrancamento( MainTree )
                dummy = input()
        if( op == "0" ):
            op = None
