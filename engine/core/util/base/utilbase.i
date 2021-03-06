/***************************************************************************
 *   Copyright (C) 2005-2019 by the FIFE team                              *
 *   http://www.fifengine.net                                              *
 *   This file is part of FIFE.                                            *
 *                                                                         *
 *   FIFE is free software; you can redistribute it and/or                 *
 *   modify it under the terms of the GNU Lesser General Public            *
 *   License as published by the Free Software Foundation; either          *
 *   version 2.1 of the License, or (at your option) any later version.    *
 *                                                                         *
 *   This library is distributed in the hope that it will be useful,       *
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU     *
 *   Lesser General Public License for more details.                       *
 *                                                                         *
 *   You should have received a copy of the GNU Lesser General Public      *
 *   License along with this library; if not, write to the                 *
 *   Free Software Foundation, Inc.,                                       *
 *   51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA          *
 ***************************************************************************/

%module fife
%{
#include "util/base/fifeclass.h"
%}

%include "util/base/exception.h"
%include "util/resource/resource.i"

namespace FIFE {

	typedef std::size_t fifeid_t;
	
	class FifeClass{
	public:
		virtual ~FifeClass();
		fifeid_t getFifeId();
	};

	%extend FifeClass {
		bool __eq__(const PyObject *other) { return false; }
		bool __ne__(const PyObject *other) { return true; }
		bool __eq__(FifeClass *other)
		{
			if (!other) return false;
			return $self->getFifeId() == other->getFifeId();
		}
		bool __ne__(FifeClass *other)
		{
			if (!other) return true;
			return $self->getFifeId() != other->getFifeId();
		}
		fifeid_t __hash__() { return $self->getFifeId(); }
	}
}
