datatype Tree<T> = Leaf | Node(Tree<T>, Tree<T>, T)
datatype List<T> = Nil | Cons(T, List<T>)

function flatten<T>(tree:Tree<T>):List<T>
ensures tree == Leaf ==> flatten(tree) == Nil
{
    match tree
        case Leaf => Nil
        case Node(t1, t2, t) => append(Cons(t, flatten(t1)), flatten(t2))
}

function append<T>(xs:List<T>, ys:List<T>):List<T>
ensures xs == Nil ==> append(xs,ys) == ys
ensures ys == Nil ==> append(xs,ys) == xs
{
	match xs
        case Nil => ys
        case Cons(x,xs') => Cons(x, append(xs',ys))
}

function treeContains<T>(tree:Tree<T>, element:T):bool
ensures tree == Leaf ==> treeContains(tree, element) == false
{
	match tree
        case Leaf => false
        case Node(t1, t2, t) => t == element || treeContains(t1, element) || treeContains(t2, element)
}

function listContains<T>(xs:List<T>, element:T):bool
ensures xs == Nil ==> listContains(xs, element) == false
{
	match xs
        case Nil => false
        case Cons(x, xs') => x == element || listContains(xs', element)
}


lemma sameElements<T>(tree:Tree<T>, element:T)
ensures treeContains(tree, element) <==> listContains(flatten(tree), element)
{
	match tree
        case Leaf => {}
        case Node(t1, t2, t) => {
            listContains(append(Cons(t, flatten(t1)), flatten(t2), element);
            assert listContains(flatten(tree), element)
                == listContains(append(Cons(t, flatten(t1)), flatten(t2)), element)
                == listContains(Cons(t, append(flatten(t1), flatten(t2))), element)
                == (t==element || listContains(append(flatten(t1), flatten(t2)), element))
                == (t==element || listContains(flatten(t1), element) || listContains(flatten(t2), element))
                == (t==element || treeContains(t1, element) || treeContains(t2, element))
                == treeContains(tree, element);
            assert treeContains(tree, element)
                == treeContains(Node(t1, t2, t), element)
                == (treeContains(t1, element) || treeContains(t2, element) || t == element)
                == (listContains(flatten(t1), element) || listContains(flatten(t2), element) || t == element)
                == listContains(append(Cons(t, flatten(t1)), flatten(t2)), element)
                == listContains(flatten(tree), element);
        }
}