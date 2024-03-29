from . import AndQuery, OrQuery, QueryComponent, TermLiteral, PhraseLiteral
from text import TokenProcessor
class BooleanQueryParser:
    class _StringBounds:
        """A wrapper class for identifying a range within a string."""
        def __init__(self, start : int, length : int):
            self.start = start
            self.length = length

    class _Literal:
        """A wrapper class for a QueryComponent and the range within a string where it was parsed from."""
        def __init__(self, bounds : 'BooleanQueryParser._StringBounds', literal_component : QueryComponent):
            self.bounds = bounds
            self.literal_component = literal_component

    @staticmethod
    def _find_next_subquery(query : str, start_index : int) -> _StringBounds:
        """
        Locates the start index and length of the next subquery in the given query string,
	    starting at the given index.
        """
        length_out = 0

        # Find the start of the next subquery by skipping spaces and + signs.
        test = query[start_index]
        while test == ' ' or test == '+':
            start_index += 1
            test = query[start_index]

        # Find the end of the next subquery.
        next_plus = query.find("+", start_index + 1)
        if next_plus < 0:
            # If there is no other + sign, then this is the final subquery in the
			# query string.
            length_out = len(query) - start_index
        else:
            # If there is another + sign, then the length of this subquery goes up
			# to the next + sign.
		
			# Move next_plus backwards until finding a non-space non-plus character.
            test = query[next_plus]
            while test == ' ' or test == '+':
                next_plus -= 1
                test = query[next_plus]

            length_out = 1 + next_plus - start_index

        # startIndex and lengthOut give the bounds of the subquery.
        return BooleanQueryParser._StringBounds(start_index, length_out) 
			
    @staticmethod
    def _find_next_literal(subquery : str, start_index : int, processor : TokenProcessor) -> 'BooleanQueryParser._Literal':
        """
        Locates and returns the next literal from the given subquery string.
        """
        sub_length = len(subquery)
        length_out = 0

        # Skip past white space.
        while subquery[start_index] == ' ':
            start_index += 1

        # Locate the next space to find the end of this literal.
        next_space = subquery.find(' ', start_index)
        if next_space < 0:
            # No more literals in this subquery.
            length_out = sub_length - start_index
        else:
            if subquery[start_index] == "\"":
                end_string = start_index
                while subquery[end_string + 1] != "\"":
                    end_string += 1
                # +2 accounts for the enclosing quotes
                length_out = (end_string + 2) - start_index
                return BooleanQueryParser._Literal(
                    BooleanQueryParser._StringBounds(start_index, length_out),
                    PhraseLiteral(subquery[start_index + 1:start_index + length_out + 1].split(" "), processor)
                )
            else:
                length_out = next_space - start_index        
        # This is a term literal containing a single term.
        return BooleanQueryParser._Literal(
            BooleanQueryParser._StringBounds(start_index, length_out),
            TermLiteral(subquery[start_index:start_index + length_out], processor)
        )

        # TODO:
		# Instead of assuming that we only have single-term literals, modify this method so it will create a PhraseLiteral
		# object if the first non-space character you find is a double-quote ("). In this case, the literal is not ended
		# by the next space character, but by the next double-quote character.
        
    def parse_query(self, query : str, processor) -> QueryComponent:
        """
        Given a boolean query, parses and returns a tree of QueryComponents representing the query.
        """
        all_subqueries = []
        start = 0

        # General routine: scan the query to identify a literal, and put that literal into a list.
		# Repeat until a + or the end of the query is encountered; build an AND query with each
		# of the literals found. Repeat the scan-and-build-AND-query phase for each segment of the
		# query separated by + signs. In the end, build a single OR query that composes all of the built
		# AND subqueries.

        while start < len(query):
            # Identify the next subquery: a portion of the query up to the next + sign.
            next_subquery = BooleanQueryParser._find_next_subquery(query, start)
            # Extract the identified subquery into its own string.
            subquery = query[next_subquery.start:next_subquery.start + next_subquery.length]
            sub_start = 0

            # Store all the individual components of this subquery.
            subquery_literals = []

            while sub_start < len(subquery):
                # Extract the next literal from the subquery.
                lit = BooleanQueryParser._find_next_literal(subquery, sub_start, processor)

                # Add the literal component to the conjunctive list.
                subquery_literals.append(lit.literal_component)

                # Set the next index to start searching for a literal.
                sub_start = lit.bounds.start + lit.bounds.length
                # Terminate once we reach the end of the query.

            # After processing all literals, we are left with a conjunctive list
			# of query components, and must fold that list into the final disjunctive list
			# of components.
			
			# If there was only one literal in the subquery, we don't need to AND it with anything --
			# its component can go straight into the list.
            if len(subquery_literals) == 1:
                all_subqueries.append(subquery_literals[0])
            else:
                # With more than one literal, we must wrap them in an AndQuery component.
                all_subqueries.append(AndQuery(subquery_literals))
          
            start = next_subquery.start + next_subquery.length
        
        # After processing all subqueries, we either have a single component or multiple components
		# that must be combined with an OrQuery.
        if len(all_subqueries) == 1:
            return all_subqueries[0]
        elif len(all_subqueries) > 1:
            return OrQuery(all_subqueries)
        else:
            return None
