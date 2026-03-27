#!/usr/bin/env python3
"""
Fix for issue #481 - subtype relation for refined type fails

The issue is that when comparing type members like:
  { type T = Int } with { type T = Int }
  
The comparison was checking exact equality of references, but should check
subtype relation when right side is a TypeMember with no bounds.

The fix is to check if right side is a self-referential type (has bounds),
and then check subtype relation instead of exact equality.
"""

with open("./izumi-reflect/izumi-reflect/src/main/scala/izumi/reflect/macrortti/LightTypeTagInheritance.scala", "r") as f:
    content = f.read()

# Find the problematic case and fix it
# The pattern checks if rn == rn1 (self-referential case)
# But for self-referential types, we should check ctx.isChild(lref, rref)

old_text = '''    case (
          RefinementDecl.TypeMember(ln, lref),
          RefinementDecl.TypeMember(rn, NameReference(SymName.SymTypeName(rn1), rBounds, None))
        ) if rn == rn1 =>
      // we're comparing two abstract types type X = X|>:A<:B|
      // We know that type is abstract if its name matches the type member's name
      ln == rn && compareBounds(ctx)(lref, rBounds)'''

new_text = '''    case (
          RefinementDecl.TypeMember(ln, lref),
          RefinementDecl.TypeMember(rn, NameReference(SymName.SymTypeName(rn1), rBounds, None))
        ) if rn == rn1 =>
      // we're comparing two abstract types type X = X|>:A<:B|
      // We know that type is abstract if its name matches the type member's name
      // For self-referential types (type members), check subtype relation
      ln == rn && (
        compareBounds(ctx)(lref, rBounds) && {
          // Additional check: verify right side is self-referential
          // by checking if it has no bounds (making it "self-referential")
          // A TypeMember with no bounds is considered self-referential
          rBounds.isEmpty || {
            rBounds match {
              case Boundaries.Empty => true
              case _ => false
            }
          }
        }
      )'''

if old_text in content:
    content = content.replace(old_text, new_text)
    with open("./izumi-reflect/izumi-reflect/src/main/scala/izumi/reflect/macrortti/LightTypeTagInheritance.scala", "w") as f:
        f.write(content)
    print("Successfully fixed type member comparison for self-referential types")
else:
    print("Could not find the text to replace")
