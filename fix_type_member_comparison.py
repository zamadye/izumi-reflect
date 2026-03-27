#!/usr/bin/env python3
"""
Apply fix for issue #481 - fix self-referential type member comparison
"""

with open("./izumi-reflect/izumi-reflect/src/main/scala/izumi/reflect/macrortti/LightTypeTagInheritance.scala", "r") as f:
    content = f.read()

# Find the problematic case and fix it
old_text = """    case (
          RefinementDecl.TypeMember(ln, lref),
          RefinementDecl.TypeMember(rn, NameReference(SymName.SymTypeName(rn1), rBounds, None))
        ) if rn == rn1 =>
      // we're comparing two abstract types type X = X|>:A<:B|
      // We know that type is abstract if its name matches the type member's name
      ln == rn && compareBounds(ctx)(lref, rBounds)
    case (RefinementDecl.TypeMember(ln, lref), RefinementDecl.TypeMember(rn, rref)) =>
      // if rhs type is not abstract (has form `type X = Int`), then lhs must be exactly equal to it, not <:
      ln == rn && lref == rref"""

new_text = """    case (
          RefinementDecl.TypeMember(ln, lref),
          RefinementDecl.TypeMember(rn, NameReference(SymName.SymTypeName(rn1), rBounds, None))
        ) if rn == rn1 =>
      // we're comparing two abstract types type X = X|>:A<:B|
      // We know that type is abstract if its name matches the type member's name
      // For type members in refinements, check if right side is self-referential
      // (has no bounds) and then verify subtype relation instead of exact equality
      val isRightSideSelfReferential = rBounds match {
        case Boundaries.Empty => true
        case _ => false
      }
      ln == rn && (isRightSideSelfReferential || ctx.isChild(lref, rref))"""

if old_text in content:
    content = content.replace(old_text, new_text)
    with open("./izumi-reflect/izumi-reflect/src/main/scala/izumi/reflect/macrortti/LightTypeTagInheritance.scala", "w") as f:
        f.write(content)
    print("Successfully fixed type member comparison for self-referential types")
else:
    print("Could not find old text - file may already be fixed")
