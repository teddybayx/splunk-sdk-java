/*
 * Copyright 2011 Splunk, Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License"): you may
 * not use this file except in compliance with the License. You may obtain
 * a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 * License for the specific language governing permissions and limitations
 * under the License.
 */

import com.splunk.Resource;

class LicensePoolNode extends ResourceNode {
    LicensePoolNode(Resource value) {
        super(value);
    }

    @Override protected PropertyList getMetadata() {
        PropertyList list = super.getMetadata();
        list.add(String.class, "getDescription");
        list.add(long.class, "getQuota");
        list.add(String[].class, "getSlaves");
        list.add(long.class, "getSlavesUsageBytes");
        list.add(String.class, "getStackId");
        list.add(long.class, "getUsedBytes");
        return list;
    }
}
